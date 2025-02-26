
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import filters, Client, errors, enums
from database import add_user, add_group, all_users, all_groups, users, remove_user
from configs import cfg
import random, asyncio

app = Client(
    "approver",
    api_id=cfg.API_ID,
    api_hash=cfg.API_HASH,
    bot_token=cfg.BOT_TOKEN
)

gif_data = {
    'https://envs.sh/eWd.jpg': {
        'caption': "🔥 Exclusive Anime Clip Just for You! 🔥",
        'button': InlineKeyboardMarkup(
            [[InlineKeyboardButton("💬 Join Anime Group", url="https://t.me/DKANIME_GROUP")]]
        )
    },
    'https://envs.sh/eWt.jpg': {
        'caption': "🚀 Don't Miss This Amazing Moment! 🚀",
        'button': InlineKeyboardMarkup(
            [[InlineKeyboardButton("🗯 Visit Our Channel", url="https://t.me/DK_ANIMES")]]
        )
    }
}

txt = [
    '<b><blockquote>😘Direct video uploaded only for you 😢\n👇👇👇👇\n➥ https://t.me/+BK7FdGsyHmk5N2Y9\n➥ https://t.me/+BK7FdGsyHmk5N2Y9\n\n𝐈𝐌𝐒𝐇𝐀 𝐑𝐄𝐇𝐌𝐀𝐍 𝐀𝐋𝐋 \n https://t.me/+BK7FdGsyHmk5N2Y9\n https://t.me/+BK7FdGsyHmk5N2Y9\n\n👉/start</blockquote></b>'
]

txt1 = [
    '**please click here /start**'
]

txt2 = [
    '**is Group pe aao na baat karte hai \n\n @DKANIME_GROUP\n @DKANIME_GROUP**',
    '**Tumhe pata hai is group pe sare anime hindi me milte hai Bas name likhne se\n\n @DKANIME_GROUP\n @DKANIME_GROUP**',
    '**please mera group join karlo \n\n @DKANIME_GROUP\n @DKANIME_GROUP**'
]

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Main process ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_chat_join_request(filters.group | filters.channel & ~filters.private)
async def approve(_, m: Message):
    op = m.chat
    kk = m.from_user
    try:
        add_group(m.chat.id)

        # 🎲 Select a random GIF and text
        selected_gif = random.choice(list(gif_data.keys()))
        gif_info = gif_data[selected_gif]
        text = random.choice(txt)
        text1 = random.choice(txt1)
        text2 = random.choice(txt2)

        # Send first text message
        await app.send_message(kk.id, text)

        # ⏳ Delay before sending text1
        await asyncio.sleep(10)
        await app.send_message(kk.id, text1)

        # Send GIF as an animation
        await app.send_animation(
            chat_id=kk.id, 
            animation=selected_gif,
            caption=gif_info["caption"], 
            reply_markup=gif_info["button"]
        )

        # ⏳ Delay before sending text2
        await asyncio.sleep(60)
        await app.send_message(kk.id, text2)

        add_user(kk.id)

    except errors.PeerIdInvalid:
        print("User hasn't started the bot yet.")
    except Exception as err:
        print(f"Error: {err}")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Start ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("start"))
async def op(_, m: Message):
    try:
        if m.chat.type == enums.ChatType.PRIVATE:
            selected_gif = random.choice(list(gif_data.keys()))
            gif_info = gif_data[selected_gif]
            selected_text = random.choice(txt1)

            add_user(m.from_user.id)

            # Send random text
            await m.reply_text(selected_text)

            # Send GIF
            await app.send_animation(
                chat_id=m.chat.id, 
                animation=selected_gif,
                caption=gif_info["caption"], 
                reply_markup=gif_info["button"]
            )

        elif m.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            add_group(m.chat.id)
            await m.reply_text(f"**🦊 Hello {m.from_user.first_name}!\nWrite to me in private for more details**")

        print(f"{m.from_user.first_name} started the bot!")

    except Exception as err:
        print(f"Error: {err}")

print("I'm Alive Now!")
app.run()



   
        
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ callback ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ info ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("users") & filters.user(cfg.SUDO))
async def dbtool(_, m : Message):
    xx = all_users()
    x = all_groups()
    tot = int(xx + x)
    await m.reply_text(text=f"""
🍀 Chats Stats 🍀
🙋‍♂️ Users : `{xx}`
👥 Groups : `{x}`
🚧 Total users & groups : `{tot}` """)

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Broadcast ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("bcast") & filters.user(cfg.SUDO))
async def bcast(_, m : Message):
    allusers = users
    lel = await m.reply_text("`⚡️ Processing...`")
    success = 0
    failed = 0
    deactivated = 0
    blocked = 0
    for usrs in allusers.find():
        try:
            userid = usrs["user_id"]
            #print(int(userid))
            if m.command[0] == "bcast":
                await m.reply_to_message.copy(int(userid))
            success +=1
        except FloodWait as ex:
            await asyncio.sleep(ex.value)
            if m.command[0] == "bcast":
                await m.reply_to_message.copy(int(userid))
        except errors.InputUserDeactivated:
            deactivated +=1
            remove_user(userid)
        except errors.UserIsBlocked:
            blocked +=1
        except Exception as e:
            print(e)
            failed +=1

    await lel.edit(f"✅Successfull to `{success}` users.\n❌ Faild to `{failed}` users.\n👾 Found `{blocked}` Blocked users \n👻 Found `{deactivated}` Deactivated users.")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Broadcast Forward ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("fcast") & filters.user(cfg.SUDO))
async def fcast(_, m : Message):
    allusers = users
    lel = await m.reply_text("`⚡️ Processing...`")
    success = 0
    failed = 0
    deactivated = 0
    blocked = 0
    for usrs in allusers.find():
        try:
            userid = usrs["user_id"]
            #print(int(userid))
            if m.command[0] == "fcast":
                await m.reply_to_message.forward(int(userid))
            success +=1
        except FloodWait as ex:
            await asyncio.sleep(ex.value)
            if m.command[0] == "fcast":
                await m.reply_to_message.forward(int(userid))
        except errors.InputUserDeactivated:
            deactivated +=1
            remove_user(userid)
        except errors.UserIsBlocked:
            blocked +=1
        except Exception as e:
            print(e)
            failed +=1

    await lel.edit(f"✅Successfull to `{success}` users.\n❌ Faild to `{failed}` users.\n👾 Found `{blocked}` Blocked users \n👻 Found `{deactivated}` Deactivated users.")

print("I'm Alive Now!")
app.run()
