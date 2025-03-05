from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from asyncio.exceptions import TimeoutError
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid
)
from configs import cfg
from database import (
    db,  # Add this line to import db instance
    set_session,
    get_session,
    delete_session,
    log_to_channel
)
import random
import string
import asyncio
import pyrogram.utils

pyrogram.utils.MIN_CHANNEL_ID = -1009147483647

# Initialize Bot Client
app = Client(
    "bot",
    api_id=cfg.API_ID,
    api_hash=cfg.API_HASH,
    bot_token=cfg.BOT_TOKEN
)

LOG_CHANNEL = cfg.LOG_CHANNEL

# Variable to control the infinite loop
changeall_running = False
SESSION_STRING_SIZE = 351

# Function to log messages in the log channel
async def log_to_channel(text: str):
    await asyncio.sleep(2)  # Delay log sending by 2 seconds
    try:
        await app.send_message(LOG_CHANNEL, text)
    except Exception as e:
        print(f"Failed to log message: {e}")

# Function to generate a random string of 2 characters (mix of letters and digits)
def generate_random_string():
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choices(characters, k=2))

# Start message
@app.on_message(filters.command("start"))
async def start_message(client: Client, message: Message):
    await message.reply_text(
        "Hello! Use the following commands:\n"
        "/create - Create a private channel.\n"
        "/change1 - Change a single channel link.\n"
        "/changeall - Start changing all channel usernames in a loop.\n"
        "/stopchangeall - Stop the change all process.\n"
        "/login - Log in with a phone number.\n"
        "/logout - Log out of the session."
    )
    await log_to_channel(f"👋 Bot started by {message.from_user.mention} (ID: {message.from_user.id})")

# LOGIN FUNCTION
@app.on_message(filters.private & filters.command(["login"]))
async def login(client: Client, message: Message):
    user_data = await db.get_session(message.from_user.id)
    if user_data is not None:
        await message.reply("You are already logged in. Please /logout first before logging in again.")
        return

    user_id = message.from_user.id

    # Ask for the phone number
    await message.reply("Please send your phone number with the country code (e.g., +1234567890).")
    phone_number_msg = await app.listen(user_id)
    phone_number = phone_number_msg.text

    new_client = Client(":memory:", cfg.API_ID, cfg.API_HASH)
    await new_client.connect()

    try:
        code = await new_client.send_code(phone_number)

        # Ask for the OTP code
        await message.reply("Please enter the OTP received on Telegram (e.g., 12345).")
        phone_code_msg = await app.listen(user_id)
        phone_code = phone_code_msg.text.replace(" ", "")

        await new_client.sign_in(phone_number, code.phone_code_hash, phone_code)

    except (PhoneNumberInvalid, PhoneCodeInvalid, PhoneCodeExpired) as e:
        await message.reply(f"Error: {str(e)}")
        return

    except SessionPasswordNeeded:
        # Ask for the 2FA password
        await message.reply("Your account has 2FA enabled. Please enter your password.")
        password_msg = await app.listen(user_id)
        try:
            await new_client.check_password(password=password_msg.text)
        except PasswordHashInvalid:
            await message.reply("Invalid Password.")
            return

    string_session = await new_client.export_session_string()
    await new_client.disconnect()

    if len(string_session) < 351:
        await message.reply("Invalid session string.")
        return

    await db.set_session(user_id, session=string_session)
    await message.reply("Account logged in successfully.")
    await log_to_channel(f"✅ User {message.from_user.mention} logged in successfully.")


# LOGOUT FUNCTION
@app.on_message(filters.command("logout"))
async def logout(client: Client, message: Message):
    user_data = get_session(message.from_user.id)
    if user_data:
        set_session(message.from_user.id, session=None)
        await message.reply("Logged out successfully.")
        await log_to_channel(f"✅ User {message.from_user.mention} logged out successfully.")

# CREATE PRIVATE CHANNEL
@app.on_message(filters.command("create"))
async def create_channel(client: Client, message: Message):
    client_user = await get_logged_in_client(message.from_user.id)
    channel = await client_user.create_channel(title="New Channel", description="Private channel created by the bot.")
    add_created_channel(channel.id)
    await message.reply(f"✅ Created channel: {channel.title}")
    await log_to_channel(f"✅ Channel '{channel.title}' created by {message.from_user.mention}")

# CHANGE 1 CHANNEL LINK
@app.on_message(filters.command("change1"))
async def change_channel_link(client: Client, message: Message):
    client_user = await get_logged_in_client(message.from_user.id)
    channels = [dialog.chat for dialog in await client_user.get_dialogs() if dialog.chat.username]
    
    if not channels:
        await message.reply("No channels with a username found.")
        return

    buttons = [
        [InlineKeyboardButton(text=channel.title, callback_data=f"change_{channel.id}")]
        for channel in channels
    ]
    await message.reply(
        "Select a channel to change its link:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# CHANGE ALL CHANNEL LINKS IN LOOP
@app.on_message(filters.command("changeall"))
async def change_all_channel_links(client: Client, message: Message):
    global changeall_running
    changeall_running = True
    client_user = await get_logged_in_client(message.from_user.id)

    while changeall_running:
        channels = [dialog.chat for dialog in await client_user.get_dialogs() if dialog.chat.username]
        for channel in channels:
            if not changeall_running:
                break

            old_username = channel.username
            new_username = f"{old_username[:-2]}{generate_random_string()}"
            await client_user.set_chat_username(channel.id, new_username)
            
            temp_channel = await client_user.create_channel(title="Temporary", description=f"Temp channel for {old_username}")
            await client_user.set_chat_username(temp_channel.id, old_username)
            add_created_channel(temp_channel.id)
            await log_to_channel(f"Temporary channel created with @{old_username}")
            
            asyncio.create_task(delete_temp_channel(temp_channel.id, client_user))
            await asyncio.sleep(3600)

# DELETE TEMPORARY CHANNEL AFTER 5 HOURS
async def delete_temp_channel(channel_id: int, client_user: Client):
    await asyncio.sleep(18000)  # 5 hours
    await client_user.delete_channel(channel_id)
    await log_to_channel(f"🗑️ Temporary channel deleted")

# STOP CHANGE ALL
@app.on_message(filters.command("stopchangeall"))
async def stop_change_all(client: Client, message: Message):
    global changeall_running
    changeall_running = False
    await message.reply("🛑 Stopped the change all process.")
    await log_to_channel("🛑 The change all process was stopped.")

# GET LOGGED IN CLIENT
async def get_logged_in_client(user_id: int) -> Client:
    user_data = get_session(user_id)
    if not user_data or not user_data['session']:
        raise Exception("User is not logged in.")
    session_string = user_data['session']
    client_user = Client(":memory:", session_string=session_string, api_id=cfg.API_ID, api_hash=cfg.API_HASH)
    await client_user.connect()
    return client_user

print("Bot Running...")

app.run()
