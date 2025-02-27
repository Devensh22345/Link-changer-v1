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

txt = ['hello']
txt1 = ['**𝐇𝐞𝐥𝐥𝐨 𝐈 𝐚𝐦 𝐚 𝐀𝐧𝐢𝐦𝐞 𝐏𝐫𝐨𝐯𝐢𝐝𝐞𝐫 𝐁𝐨𝐭 𝐛𝐲 [@DK_ANIMES]**']
txt2 = [
    '<b><blockquote> 𝐂𝐥𝐢𝐜𝐤 𝐇𝐞𝐫𝐞 𝐭𝐨 𝐆𝐞𝐭 𝐀𝐧𝐢𝐦𝐞 𝐢𝐧 𝐇𝐢𝐧𝐝𝐢 \n𝐉𝐮𝐬𝐭 𝐂𝐥𝐢𝐜𝐤 𝐨𝐧 👇👇 </blockquote>\n /START</b>'
]

@app.on_chat_join_request(filters.group | filters.channel & ~filters.private)
async def approve(_, m: Message):
    op = m.chat
    kk = m.from_user
    try:
        add_group(m.chat.id)
        print(f"Received join request from {kk.id} in {op.id}")

        # Image URL
        img = "https://envs.sh/elk.jpg"

        # Inline Keyboard
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("𝐂𝐥𝐢𝐜𝐤 𝐡𝐞𝐫𝐞 𝐓𝐨 𝐖𝐚𝐭𝐜𝐡/𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝 𝐢𝐧 𝐇𝐢𝐧𝐝𝐢 👀", url="https://t.me/leveling_solo_robot?start=hi")],
                [InlineKeyboardButton("𝐍𝐞𝐰 𝐚𝐧𝐢𝐦𝐞 𝐢𝐧 𝐇𝐢𝐧𝐝𝐢", url="https://t.me/leveling_solo_robot?start=hi")],
            ]
        )

        text1 = random.choice(txt1)
        text2 = random.choice(txt2)

        await app.send_message(kk.id, text1)
        await app.send_message(kk.id, text2)
        await app.send_photo(
            kk.id,
            img,
            caption="<b><blockquote>𝐂𝐥𝐢𝐜𝐤 𝐨𝐧 𝐁𝐞𝐥𝐨𝐰 𝐁𝐮𝐭𝐭𝐨𝐧 𝐓𝐨 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝 𝐘𝐨𝐮𝐫 𝐄𝐩𝐢𝐬𝐨𝐝𝐞 👇👇👇👇</blockquote></b>",
            reply_markup=keyboard
        )

        add_user(kk.id)

    except errors.PeerIdInvalid:
        print("User hasn't started the bot yet.")
    except Exception as err:
        print(f"Error: {err}")


@app.on_message(filters.command("start"))
async def start(_, m: Message):
    try:
        user = m.from_user

        # Send a log message to your log channel
        log_text = f"👤 <b>User Started Bot</b>\n" \
                   f"🆔 ID: <code>{user.id}</code>\n" \
                   f"👤 Name: {user.full_name}\n" \
                   f"🔗 Username: @{user.username}" if m.from_user.username else 'None'

        await app.send_message(cfg.LOG_CHANNEL, log_text)
        
        if m.chat.type == enums.ChatType.PRIVATE:
            keyboard = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("𝐀𝐧𝐢𝐦𝐞 𝐢𝐧 𝐇𝐢𝐧𝐝𝐢", url="https://t.me/+2fsV4nzHvOs2OGNl")],
                    [InlineKeyboardButton("𝐒𝐨𝐥𝐨 𝐋𝐞𝐯𝐞𝐥𝐢𝐧𝐠", url="https://t.me/+BYFsBvSb8eM5ZTc1")],
                    [InlineKeyboardButton("𝐍𝐚𝐫𝐮𝐭𝐨 𝐬𝐡𝐢𝐩𝐩𝐮𝐝𝐞𝐧", url="https://t.me/+1Uqfi_EB69s3MDVl")],
                    [InlineKeyboardButton("𝐃𝐞𝐦𝐨𝐧 𝐬𝐥𝐚𝐲𝐞𝐫", url="https://t.me/+-Uh3oEL5NKBjMzZl")],
                    [InlineKeyboardButton("𝐀𝐭𝐭𝐚𝐜𝐤 𝐨𝐧 𝐓𝐢𝐭𝐚𝐧", url="https://t.me/+bxKksmx6D5I5ZmNl")],
                    [InlineKeyboardButton("𝐃𝐞𝐚𝐭𝐡 𝐧𝐨𝐭𝐞", url="https://t.me/+llU_niDFQxwxYTJl")]
                ]
            )

            add_user(user.id)
            await m.reply_photo(
                "https://envs.sh/elk.jpg",
                caption=f"<b><blockquote>𝐂𝐥𝐢𝐜𝐤 𝐨𝐧 𝐓𝐡𝐞 𝐚𝐧𝐢𝐦𝐞 𝐍𝐚𝐦𝐞 \n𝐓𝐨 𝐃𝐢𝐫𝐞𝐜𝐭 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝 𝐘𝐨𝐮𝐫 𝐀𝐧𝐢𝐦𝐞.🔥🔥</blockquote></b>\n\n<b><blockquote>𝐈𝐅 𝐲𝐨𝐮 𝐃𝐢𝐝𝐧'𝐭 𝐅𝐢𝐧𝐝 𝐲𝐨𝐮𝐫 𝐚𝐧𝐢𝐦𝐞 𝐢𝐧 𝐓𝐡𝐢𝐬 𝐥𝐢𝐬𝐭 𝐓𝐡𝐞𝐧 𝐉𝐨𝐢𝐧 [@DKANIME_GROUP] 𝐚𝐧𝐝 𝐉𝐮𝐬𝐭 𝐓𝐲𝐩𝐞 𝐲𝐨𝐮𝐫 𝐚𝐧𝐢𝐦𝐞 𝐍𝐚𝐦𝐞 𝐇𝐞𝐫𝐞.</blockquote></b>",
                reply_markup=keyboard
            )

        elif m.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            keyboard = InlineKeyboardMarkup(
                [[InlineKeyboardButton("💁‍♂️ Start me private 💁‍♂️", url="https://t.me/leveling_solo_robot?start=hi")]]
            )
            add_group(m.chat.id)
            await m.reply_text(f"**🦊 Hello {user.first_name}!\nWrite me in private for more details**", reply_markup=keyboard)

        print(f"{user.first_name} started the bot!")

    except Exception as err:
        print(f"Error: {err}")


@app.on_message(filters.command("users") & filters.user(cfg.SUDO))
async def dbtool(_, m: Message):
    xx = all_users()
    x = all_groups()
    tot = int(xx + x)
    await m.reply_text(text=f"""
🍀 Chats Stats 🍀
🙋‍♂️ Users : `{xx}`
👥 Groups : `{x}`
🚧 Total users & groups : `{tot}` """)


@app.on_message(filters.command("bcast") & filters.user(cfg.SUDO))
async def bcast(_, m: Message):
    allusers = users
    lel = await m.reply_text("`⚡️ Processing...`")
    success = 0
    failed = 0
    deactivated = 0
    blocked = 0

    for usrs in allusers.find():
        try:
            userid = usrs["user_id"]
            await m.reply_to_message.copy(int(userid))
            success += 1
        except FloodWait as ex:
            await asyncio.sleep(ex.value)
            await m.reply_to_message.copy(int(userid))
        except errors.InputUserDeactivated:
            deactivated += 1
            remove_user(userid)
        except errors.UserIsBlocked:
            blocked += 1
        except Exception as e:
            print(e)
            failed += 1

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
