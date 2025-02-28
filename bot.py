
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
    'https://envs.sh/iGM.mp4': {
        'caption': "𝐈𝐧𝐬𝐭𝐚𝐧𝐭 𝐕𝐢𝐫𝐚𝐥 𝐌𝐨𝐝𝐞𝐥 𝐕𝐢𝐝𝐞𝐨 🥵🥵\n\n 𝐂𝐥𝐢𝐜𝐤 𝐎𝐧 𝐁𝐞𝐥𝐨𝐰 👇👇 𝐁𝐮𝐭𝐭𝐨𝐧 \n𝐓𝐨 𝐆𝐞𝐭 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝 𝐋𝐢𝐧𝐤 💋",
        'button': InlineKeyboardMarkup(
            [[InlineKeyboardButton("💦 𝐆𝐄𝐓 𝐃𝐎𝐖𝐍𝐋𝐎𝐀𝐃 𝐋𝐈𝐍𝐊🍑", url="https://t.me/video_call_robot?start")]]
        )
    },
    'https://envs.sh/iGX.mp4': {
        'caption': "𝐈𝐧𝐬𝐭𝐚𝐧𝐭 𝐕𝐢𝐫𝐚𝐥 𝐕𝐢𝐝𝐞𝐨 🥵🥵\n\n 𝐂𝐥𝐢𝐜𝐤 𝐎𝐧 𝐁𝐞𝐥𝐨𝐰 👇👇 𝐁𝐮𝐭𝐭𝐨𝐧 \n𝐓𝐨 𝐆𝐞𝐭 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝 𝐋𝐢𝐧𝐤 💋",
        'button': InlineKeyboardMarkup(
            [[InlineKeyboardButton("💦 𝐆𝐄𝐓 𝐃𝐎𝐖𝐍𝐋𝐎𝐀𝐃 𝐋𝐈𝐍𝐊🍑", url="https://t.me/video_call_robot?start")]]
        )
    },
    'https://envs.sh/iG6.mp4': {
        'caption': "𝐈𝐧𝐬𝐭𝐚𝐧𝐭 𝐕𝐢𝐫𝐚𝐥 𝐕𝐢𝐝𝐞𝐨 🥵🥵\n\n 𝐂𝐥𝐢𝐜𝐤 𝐎𝐧 𝐁𝐞𝐥𝐨𝐰 👇👇 𝐁𝐮𝐭𝐭𝐨𝐧 \n𝐓𝐨 𝐆𝐞𝐭 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝 𝐋𝐢𝐧𝐤 💋",
        'button': InlineKeyboardMarkup(
            [[InlineKeyboardButton("💦 𝐆𝐄𝐓 𝐃𝐎𝐖𝐍𝐋𝐎𝐀𝐃 𝐋𝐈𝐍𝐊🍑", url="https://t.me/video_call_robot?start")]]
        )
    },
    'https://envs.sh/iKh.mp4': {
        'caption': "𝐈𝐧𝐬𝐭𝐚𝐧𝐭 𝐕𝐢𝐫𝐚𝐥 𝐌𝐨𝐝𝐞𝐥 𝐕𝐢𝐝𝐞𝐨 🥵🥵\n\n 𝐂𝐥𝐢𝐜𝐤 𝐎𝐧 𝐁𝐞𝐥𝐨𝐰 👇👇 𝐁𝐮𝐭𝐭𝐨𝐧 \n𝐓𝐨 𝐆𝐞𝐭 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝 𝐋𝐢𝐧𝐤 💋",
        'button': InlineKeyboardMarkup(
            [[InlineKeyboardButton("💦 𝐆𝐄𝐓 𝐃𝐎𝐖𝐍𝐋𝐎𝐀𝐃 𝐋𝐈𝐍𝐊🍑", url="https://t.me/video_call_robot?start")]]
        )
    },
    'https://envs.sh/iK2.mp4': {
        'caption': "𝐈𝐧𝐬𝐭𝐚𝐧𝐭 𝐕𝐢𝐫𝐚𝐥 𝐌𝐨𝐝𝐞𝐥 𝐕𝐢𝐝𝐞𝐨 🥵🥵\n\n 𝐂𝐥𝐢𝐜𝐤 𝐎𝐧 𝐁𝐞𝐥𝐨𝐰 👇👇 𝐁𝐮𝐭𝐭𝐨𝐧 \n𝐓𝐨 𝐆𝐞𝐭 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝 𝐋𝐢𝐧𝐤 💋",
        'button': InlineKeyboardMarkup(
            [[InlineKeyboardButton("💦 𝐆𝐄𝐓 𝐃𝐎𝐖𝐍𝐋𝐎𝐀𝐃 𝐋𝐈𝐍𝐊🍑", url="https://t.me/video_call_robot?start")]]
        )
    },
    'https://envs.sh/iKF.mp4': {
        'caption': "𝐈𝐧𝐬𝐭𝐚𝐧𝐭 𝐕𝐢𝐫𝐚𝐥 𝐌𝐨𝐝𝐞𝐥 𝐕𝐢𝐝𝐞𝐨 🥵🥵\n\n 𝐂𝐥𝐢𝐜𝐤 𝐎𝐧 𝐁𝐞𝐥𝐨𝐰 👇👇 𝐁𝐮𝐭𝐭𝐨𝐧 \n𝐓𝐨 𝐆𝐞𝐭 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝 𝐋𝐢𝐧𝐤 💋",
        'button': InlineKeyboardMarkup(
            [[InlineKeyboardButton("💦 𝐆𝐄𝐓 𝐃𝐎𝐖𝐍𝐋𝐎𝐀𝐃 𝐋𝐈𝐍𝐊🍑", url="https://t.me/video_call_robot?start")]]
        )
    }
}


txt = [
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
        text2 = random.choice(txt2)

        # Send first text message
        await app.send_message(kk.id, text)        
   
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



#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Start Command ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("start"))
async def op(_, m: Message):
    try:
        if m.chat.type == enums.ChatType.PRIVATE:
            selected_gif = random.choice(list(gif_data.keys()))
            gif_info = gif_data[selected_gif]
            selected_text = random.choice(txt)

            add_user(m.from_user.id)

            await m.reply_text(selected_text)

            await app.send_animation(
                chat_id=m.from_user.id,  # Use from_user.id for private chat
                animation=selected_gif,
                caption=gif_info["caption"],
                reply_markup=gif_info["button"]
            )

            # Log new user to LOG_CHANNEL
            try:
                log_msg = (
                    f"📢 **New User Started Bot**\n\n"
                    f"👤 Name: [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n"
                    f"🆔 User ID: `{m.from_user.id}`\n"
                    f"🌍 Username: @{m.from_user.username if m.from_user.username else 'None'}"
                )
                await app.send_message(cfg.LOG_CHANNEL, log_msg)

            except errors.PeerIdInvalid:
                print("⚠️ LOG_CHANNEL ID is invalid or the bot isn't an admin there.")
            except Exception as err:
                print(f"Error in logging: {err}")

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
