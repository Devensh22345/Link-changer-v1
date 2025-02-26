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

txt = [
    '<b><blockquote>😘Direct video uploaded only for you 😢\n👇👇👇👇\n➥ https://t.me/+L_bG5fjI-vU5OTBl\n➥ https://t.me/+L_bG5fjI-vU5OTBl\n\n𝐈𝐌𝐒𝐇𝐀 𝐑𝐄𝐇𝐌𝐀𝐍 𝐀𝐋𝐋 \n https://t.me/+L_bG5fjI-vU5OTBl\n https://t.me/+L_bG5fjI-vU5OTBl\n\n👉/start</blockquote></b>'
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
        img = random.choice(gif)
        text = random.choice(txt)
        text1 = random.choice(txt1)
        text2 = random.choice(txt2)
        await app.send_message(kk.id, text)
        await app.send_message(kk.id, text1)
        await app.send_video(kk.id, img)
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
        user = m.from_user
        await app.get_chat_member(cfg.CHID, user.id) 
        
        # Log the start event in the log channel
        log_message = f"🚀 **Bot Started**\n👤 User: [{user.first_name}](tg://user?id={user.id})\n🆔 User ID: `{user.id}`\n📅 Date: {m.date}"
        await app.send_message(cfg.LOG_CHANNEL, log_message)

        if m.chat.type == enums.ChatType.PRIVATE:
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("𝐀𝐧𝐢𝐦𝐞 𝐢𝐧 𝐇𝐢𝐧𝐝𝐢", url="https://t.me/+2fsV4nzHvOs2OGNl")
                    ],[
                        InlineKeyboardButton("𝐒𝐨𝐥𝐨 𝐋𝐞𝐯𝐞𝐥𝐢𝐧𝐠", url="https://t.me/+BYFsBvSb8eM5ZTc1")
                    ],[
                        InlineKeyboardButton("𝐍𝐚𝐫𝐮𝐭𝐨 𝐬𝐡𝐢𝐩𝐩𝐮𝐝𝐞𝐧", url="https://t.me/+1Uqfi_EB69s3MDVl")
                    ],[
                        InlineKeyboardButton("𝐃𝐞𝐦𝐨𝐧 𝐬𝐥𝐚𝐲𝐞𝐫", url="https://t.me/+-Uh3oEL5NKBjMzZl")
                    ],[
                        InlineKeyboardButton("𝐀𝐭𝐭𝐚𝐜𝐤 𝐨𝐧 𝐓𝐢𝐭𝐚𝐧", url="https://t.me/+bxKksmx6D5I5ZmNl")
                ],[
                        InlineKeyboardButton("𝐃𝐞𝐚𝐭𝐡 𝐧𝐨𝐭𝐞", url="https://t.me/+llU_niDFQxwxYTJl")
                    ] ]
            add_user(user.id)
            await m.reply_photo(
                "https://envs.sh/E-7.jpg",
                caption=f"**🦊 Hello {user.mention}!\nI'm an auto approve [Admin Join Requests](https://t.me/telegram/153) Bot.\nI can approve users in Groups/Channels. Add me to your chat and promote me to admin with add members permission.\n\n__Powered By : @DK_ANIMES**",
                reply_markup=keyboard
            )
    
        elif m.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            keyboard = InlineKeyboardMarkup(
                [[InlineKeyboardButton("💁‍♂️ Start me private 💁‍♂️", url="https://t.me/Dk_auto_request_appove_bot?startgroup")]]
            )
            add_group(m.chat.id)
            await m.reply_text(f"**🦊 Hello {user.first_name}!\nWrite me in private for more details**", reply_markup=keyboard)

        print(f"{user.first_name} started the bot!")

    except UserNotParticipant:
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🍀 Check Again 🍀", "chk")]])
        await m.reply_text(f"**⚠️ Access Denied! ⚠️\n\nPlease Join @{cfg.FSUB} to use me. If you joined, click the check again button to confirm.**", reply_markup=keyboard)
        

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ callback ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_callback_query(filters.regex("chk"))
async def chk(_, cb : CallbackQuery):
    try:
        await app.get_chat_member(cfg.CHID, cb.from_user.id)
        if cb.message.chat.type == enums.ChatType.PRIVATE:
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🗯 Channel", url="https://t.me/DK_ANIMES"),
                        InlineKeyboardButton("💬 Support", url="https://t.me/DKANIME_HINDI")
                    ],[
                        InlineKeyboardButton("➕ Add me to your Chat ➕", url="https://t.me/Dk_auto_request_appove_bot?startgroup")
                    ]
                ]
            )
            add_user(cb.from_user.id)
            await cb.message.edit("**🦊 Hello {}!\nI'm an auto approve [Admin Join Requests]({}) Bot.\nI can approve users in Groups/Channels.Add me to your chat and promote me to admin with add members permission.\n\n__Powerd By : @DK_ANIMES**".format(cb.from_user.mention, "https://t.me/telegram/153"), reply_markup=keyboard, disable_web_page_preview=True)
        print(cb.from_user.first_name +" Is started Your Bot!")
    except UserNotParticipant:
        await cb.answer("🙅‍♂️ You are not joined to channel join and try again. 🙅‍♂️")

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
