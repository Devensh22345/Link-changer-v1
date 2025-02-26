from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram import filters, Client, errors, enums
from pyrogram.errors import UserNotParticipant
from pyrogram.errors.exceptions.flood_420 import FloodWait
from database import add_user, add_group, all_users, all_groups, users, remove_user
from configs import cfg 
import random, asyncio

app = Client(
    "approver",
    api_id=cfg.API_ID,
    api_hash=cfg.API_HASH,
    bot_token=cfg.BOT_TOKEN
)

gif = [
    'https://envs.sh/E-c.mp4',
    'https://envs.sh/E-c.mp4'
 
]

gif_data = {
    'https://envs.sh/E-c.mp4': {
        'caption': "🔥 Exclusive Anime Clip Just for You! 🔥",
        'button': InlineKeyboardMarkup(
            [[InlineKeyboardButton("💬 Join Anime Group", url="https://t.me/DKANIME_GROUP")]]
        )
    },
    'https://envs.sh/E-d.mp4': {
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
        print(f"Received join request from {kk.id} in {op.id}")  # Debugging line

        # Bot will NOT approve the request
        # await app.approve_chat_join_request(op.id, kk.id)  # REMOVE THIS LINE

        # Bot can still message the user if needed
        # Select a random GIF and get its corresponding data
        selected_gif = random.choice(list(gif_data.keys()))
        gif_info = gif_data[selected_gif]
        
        text = random.choice(txt)
        text1 = random.choice(txt1)
        text2 = random.choice(txt2)

        await app.send_message(kk.id, text)
        await app.send_message(kk.id, text1)
        await app.send_video(kk.id, selected_gif, caption=gif_info['caption'], reply_markup=gif_info['button'])
        await app.send_message(kk.id, text2)
        add_user(kk.id)


    except errors.PeerIdInvalid:
        print("User hasn't started the bot yet.")
    except Exception as err:
        print(f"Error: {err}")


 
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Start ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


@app.on_message(filters.command("start"))
async def op(_, m: Message):
    if m.chat.type == enums.ChatType.PRIVATE:
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🗯 Channel", url="https://t.me/DK_ANIMES"),
                    InlineKeyboardButton("💬 Support", url="https://t.me/DKANIME_GROUP")
                ],
                [
                    InlineKeyboardButton("➕ Add me to your Chat ➕", url="https://t.me/Dk_auto_request_appove_bot?startgroup")
                ]
            ]
        )
        add_user(m.from_user.id)
        await m.reply_photo(
            "https://envs.sh/E-7.jpg",
            caption="**🦊 Hello {}!\nI'm an auto approve [Admin Join Requests]({}) Bot.\nI can approve users in Groups/Channels. Add me to your chat and promote me to admin with add members permission.\n\n__Powered By: @DK_ANIMES**".format(m.from_user.mention, "https://t.me/telegram/153"),
            reply_markup=keyboard
        )

    elif m.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("💁‍♂️ Start me in private 💁‍♂️", url="https://t.me/Dk_auto_request_appove_bot?startgroup")
                ]
            ]
        )
        add_group(m.chat.id)
        await m.reply_text("**🦊 Hello {}!\nWrite to me in private for more details.**".format(m.from_user.first_name), reply_markup=keyboard)

    print(m.from_user.first_name + " started your bot!")


   
        
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
