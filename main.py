from pyrogram import Client, filters
from pyrogram.types import *
from pymongo import MongoClient
import random
import os
import re
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Environment Variables ---
API_ID = os.environ.get("API_ID", "9999999") # Replace with your actual value
API_HASH = os.environ.get("API_HASH", "abcd1234567890") # Replace with your actual value
BOT_TOKEN = os.environ.get("BOT_TOKEN", "123456789:AA_your_bot_token_here") # Replace with your actual value
MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017/") # Replace with your actual value
BOT_IMAGE = os.environ.get("BOT_IMAGE", "https://telegra.ph/file/example_photo_id.jpg")
BOT_USERNAME = os.environ.get("BOT_USERNAME", "my_rin_chatbot")
OWNER_USERNAME = os.environ.get("OWNER_USERNAME", "owner_taki_ji")
SUPPORT_GROUP = os.environ.get("SUPPORT_GROUP", "anime_x_god_group")
UPDATES_CHANNEL = os.environ.get("UPDATES_CHANNEL", "updates_channel")


# --- Global MongoDB Client Initialization (Optimization) ---
try:
    mongo_client = MongoClient(MONGO_URL)
    v_collection = mongo_client["vDb"]["v"]
    chat_collection = mongo_client["Word"]["WordDb"]
    print("MongoDB connection successful.")
except Exception as e:
    print(f"MongoDB connection failed: {e}")
    # Bot will likely fail if DB connection is critical, but we continue for now

# --- Pyrogram Client Initialization ---
bot = Client(
    "V_Chat_Bot" ,
    api_id = API_ID,
    api_hash = API_HASH ,
    bot_token = BOT_TOKEN
)


async def is_admins(chat_id: int):
    """Checks if a user is an administrator in a chat."""
    try:
        return [
            member.user.id
            async for member in bot.iter_chat_members(
                chat_id, filter="administrators"
            )
        ]
    except Exception:
        # Handle cases where bot might not have permission
        return []

# --- Helper function for fetching replies (for clean code) ---
async def get_ai_response(word: str):
    """Fetches a random reply from the chat database based on the input word/sticker ID."""
    K = []
    is_chat = chat_collection.find({"word": word})
    k = chat_collection.find_one({"word": word})
    
    if k:
        for x in is_chat:
            K.append(x['text'])
        
        if K:
            hey = random.choice(K)
            is_text = chat_collection.find_one({"text": hey})
            if is_text:
                return hey, is_text.get('check', 'none') # returns (reply_text/file_id, check_type)
    return None, None # No response found


# --- Command Handlers ---

@bot.on_message(filters.command("start") & filters.private & ~filters.edited)
async def start_private(client: Client, message: Message):
    await message.reply_photo(
        photo=f"{BOT_IMAGE}",
        caption=f"""**━━━━━━━━━━━━━━━━━━━━━━━━
💥 𝐇𝐢  𝐈'𝐦 𝐀 𝐀𝐝𝐯𝐚𝐧𝐜𝐞 𝐂𝐡𝐚𝐭 𝐁𝐨𝐭 🌷.\n\n📌 𝐌𝐲 𝐍𝐚𝐦𝐞 𝐈𝐬 𝐑𝐈𝐍🦋⃤🇦𝐧𝐢𝐦𝐞𝐱✨ 🌷 𝐅𝐨𝐫𝐦 𝐈𝐧𝐝𝐢𝐚 🇮🇳 \n\n🌷 𝐈'𝐦 𝐀 𝐀𝐫𝐭𝐢𝐟𝐢𝐜𝐢𝐚𝐥 𝐈𝐧𝐭𝐞𝐥𝐥𝐢𝐠𝐞𝐧𝐜𝐞 🌷\n\n /chatbot - [on|off] 𝐓𝐡𝐢𝐬 𝐂𝐨𝐦𝐦𝐚𝐧𝐝 𝐔𝐬𝐞 𝐎𝐧𝐥𝐲 𝐀𝐧𝐲 𝐆𝐫𝐨𝐮𝐩

┏━━━━━━━━━━━━━━━━━┓
┣❥︎ ♕︎𝐎𝐰𝐧𝐞𝐫♕︎   » [𝐂𝐥𝐢𝐜𝐤 𝐇𝐞𝐫𝐞](https://t.me/{OWNER_USERNAME})
┣❥︎ 𝐔𝐩𝐝𝐚𝐭𝐞𝐬 ➪ » [𝐂𝐥𝐢𝐜𝐤 𝐇𝐞𝐫𝐞](https://t.me/{UPDATES_CHANNEL})
┣❥︎ 𝐒𝐮𝐩𝐩𝐨𝐫𝐭 ➪ » [𝐂𝐥𝐢𝐜𝐤 𝐇𝐞𝐫𝐞](https://t.me/{SUPPORT_GROUP})
┣❥︎ 𝐂𝐫𝐞𝐚𝐭𝐨𝐫 ➪ » [𝐓𝐚𝐤𝐢 𝐉𝐢](https://t.me/anime_fan_owner)
┗━━━━━━━━━━━━━━━━━┛

💞 𝐉𝐮𝐬𝐭 𝐀𝐝𝐝 𝐌𝐞 » 𝐓𝐨 𝐘𝐨𝐮𝐫 𝐆𝐫𝐨𝐮𝐩 𝐀𝐧𝐝
𝐄𝐧𝐣𝐨𝐲 𝐒𝐮𝐩𝐞𝐫 𝐐𝐮𝐚𝐥𝐢𝐭𝐲 ❥︎𝐂𝐡𝐚𝐭.
━━━━━━━━━━━━━━━━━━━━━━━━**""",
    reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "➕ ❰ 𝐀𝐝𝐝 𝐌𝐞 𝐓𝐨 𝐘𝐨𝐮𝐫 𝐆𝐫𝐨𝐮𝐩 ❱ ➕", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
                ]
                
           ]
        ),
    )
    
    
@bot.on_message(filters.command(["/start", f"start@{BOT_USERNAME}", "/alive", ".alive", "#taki", "#gojo"]) & filters.group & ~filters.edited)
async def start_group(client: Client, message: Message):
    await message.reply_photo(
        photo=f"{BOT_IMAGE}",
        caption=f"""💥 𝐇𝐢! 𝐈'𝐦 𝐀 𝐀𝐝𝐯𝐚𝐧𝐜𝐞 𝐂𝐡𝐚𝐭 𝐁𝐨𝐭 🌷.\n\n📌 𝐌𝐲 𝐍𝐚𝐦𝐞 𝐈𝐬 𝐑𝐈𝐍🦋⃤🇦𝐧𝐢𝐦𝐞𝐱✨ 🌷 𝐅𝐨𝐫𝐦 𝐈𝐧𝐝𝐢𝐚 🇮🇳 \n\n🌷 𝐈'𝐦 𝐀 𝐀𝐫𝐭𝐢𝐟𝐢𝐜𝐢𝐚𝐥 𝐈𝐧𝐭𝐞𝐥𝐥𝐢𝐠𝐞𝐧𝐜𝐞 🌷\n\n𝐀𝐧𝐲 𝐏𝐫𝐨𝐛𝐥𝐞𝐦 𝐓𝐨 [𝐑𝐞𝐩𝐨𝐫𝐭](https://t.me/anime_fan_owner)  🥀\n\n[𝐔𝐩𝐝𝐚𝐭𝐞𝐬](https://t.me/{UPDATES_CHANNEL}) 🌷\n\n /chatbot - [on|off]""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        " 💥 𝐉𝐨𝐢𝐧 𝐎𝐮𝐫 𝐂𝐡𝐚𝐭 𝐆𝐫𝐨𝐮𝐩 💞", url=f"https://t.me/{SUPPORT_GROUP}")
                ]
            ]
        ),
    )


@bot.on_message(
    filters.command("chatbot off", prefixes=["/", ".", "?", "-"])
    & ~filters.private)
async def chatbotofd(client, message):
    chat_id = message.chat.id
    if message.from_user:
        user = message.from_user.id
        if user not in (
           await is_admins(chat_id)
        ):
           return await message.reply_text(
                "💥 𝐇𝐞𝐲 𝐘𝐨𝐮 𝐀𝐫𝐞 𝐍𝐨𝐭 𝐀 𝐀𝐝𝐦𝐢𝐧 💥" # Consistent language recommended
            )
    is_v = v_collection.find_one({"chat_id": chat_id})
    if not is_v:
        v_collection.insert_one({"chat_id": chat_id})
        await message.reply_text(f"🌷 𝐑𝐈𝐍🦋⃤🇦𝐧𝐢𝐦𝐞𝐱✨ 𝐃𝐢𝐬𝐚𝐛𝐥𝐞𝐝 🥀!\n\n𝐀𝐧𝐲 𝐏𝐫𝐨𝐛𝐥𝐞𝐦 𝐓𝐨 [𝐑𝐞𝐩𝐨𝐫𝐭](https://t.me/anime_fan_owner)  🥀\n\n[𝐔𝐩𝐝𝐚𝐭𝐞𝐬](https://t.me/{UPDATES_CHANNEL}) 🌷")
    else: # Use else instead of repeating 'if is_v'
        await message.reply_text(f"🌷𝐑𝐈𝐍🦋⃤🇦𝐧𝐢𝐦𝐞𝐱✨ 𝐈𝐬 𝐀𝐥𝐫𝐞𝐚𝐝𝐲 𝐃𝐢𝐬𝐚𝐛𝐥𝐞𝐝 🥀!\n\n𝐀𝐧𝐲 𝐏𝐫𝐨𝐛𝐥𝐞𝐦 𝐓𝐨 [𝐑𝐞𝐩𝐨𝐫𝐭](https://t.me/anime_fan_owner)  🥀\n\n[𝐔𝐩𝐝𝐚𝐭𝐞𝐬](https://t.me/{UPDATES_CHANNEL}) 🌷")
    

@bot.on_message(
    filters.command("chatbot on", prefixes=["/", ".", "?", "-"])
    & ~filters.private)
async def chatboton(client, message):
    chat_id = message.chat.id
    if message.from_user:
        user = message.from_user.id
        if user not in (
            await is_admins(chat_id)
        ):
            return await message.reply_text(
                "💥 𝐇𝐞𝐲 𝐘𝐨𝐮 𝐀𝐫𝐞 𝐍𝐨𝐭 𝐀 𝐀𝐝𝐦𝐢𝐧 💥"
            )
    is_v = v_collection.find_one({"chat_id": chat_id})
    if not is_v:           
        await message.reply_text(f"💥 𝐑𝐈𝐍🦋⃤🇦𝐧𝐢𝐦𝐞𝐱✨ 𝐈𝐬 𝐀𝐥𝐫𝐞𝐚𝐝𝐲 𝐄𝐧𝐚𝐛𝐥𝐞𝐝 🌷!\n\n𝐀𝐧𝐲 𝐏𝐫𝐨𝐛𝐥𝐞𝐦 𝐓𝐨 [𝐑𝐞𝐩𝐨𝐫𝐭](https://t.me/anime_fan_owner)  🥀\n\n[𝐔𝐩𝐝𝐚𝐭𝐞𝐬](https://t.me/{UPDATES_CHANNEL}) 🌷")
    else: # Use else instead of repeating 'if is_v'
        v_collection.delete_one({"chat_id": chat_id})
        await message.reply_text(f"💥 𝐑𝐈𝐍🦋⃤🇦𝐧𝐢𝐦𝐞𝐱✨ 𝐈𝐬 𝐄𝐧𝐚𝐛𝐥𝐞𝐝 🌷!\n\n𝐀𝐧𝐲 𝐏𝐫𝐨𝐛𝐥𝐞𝐦 𝐓𝐨 [𝐑𝐞𝐩𝐨𝐫𝐭](https://t.me/anime_fan_owner)  🥀\n\n[𝐔𝐩𝐝𝐚𝐭𝐞𝐬](https://t.me/{UPDATES_CHANNEL}) 🌷")
    

@bot.on_message(
    filters.command("chatbot", prefixes=["/", ".", "?", "-"])
    & ~filters.private)
async def chatbot_usage(client, message):
    await message.reply_text(f"**🇮🇳 𝐔𝐬𝐚𝐠𝐞 🌷 :**\n/chatbot [on|off] 𝐎𝐧𝐥𝐲 𝐆𝐫𝐨𝐮𝐩 🇮🇳 !\n\n𝐀𝐧𝐲 𝐏𝐫𝐨𝐛𝐥𝐞𝐦 𝐓𝐨 [𝐑𝐞𝐩𝐨𝐫𝐭](https://t.me/anime_fan_owner)  🥀\n\n[𝐔𝐩𝐝𝐚𝐭𝐞𝐬](https://t.me/{UPDATES_CHANNEL}) 🌷")


# --- Group Chat/Autoreply Logic (Text/Reply) ---

@bot.on_message(
 (
        filters.text
        | filters.sticker
    )
    & ~filters.private
    & ~filters.bot,
)
async def vai(client: Client, message: Message):
    getme = await bot.get_me()
    bot_id = getme.id                             
    is_v = v_collection.find_one({"chat_id": message.chat.id})
    
    # 1. New Message (No Reply)
    if not message.reply_to_message:
       if not is_v: # Chatbot is ENABLED (entry not in v_collection means it's ON)
           await bot.send_chat_action(message.chat.id, "typing")
           word = message.text if message.text else message.sticker.file_unique_id
           reply, Yo = await get_ai_response(word)

           if reply:               
               if Yo == "sticker":
                   await message.reply_sticker(reply)
               else: # Yo == "none" or "text"
                   await message.reply_text(reply)
   
    # 2. Reply Message (Learning/Replying)
    if message.reply_to_message:  
       
       # Bot is replied to: Learning Logic
       if not message.reply_to_message.from_user.id == bot_id:          
           
           # Determine the 'word' (what the bot should learn to respond to)
           word_to_learn = None
           if message.reply_to_message.text:
               word_to_learn = message.reply_to_message.text
           elif message.reply_to_message.sticker:
               word_to_learn = message.reply_to_message.sticker.file_unique_id
               
           if word_to_learn:
               # Determine the 'text' (the response)
               if message.sticker:
                   # Learning: word (text/sticker ID) -> text (sticker file_id)
                   chat_collection.insert_one({"word": word_to_learn, "text": message.sticker.file_id, "check": "sticker", "id": message.sticker.file_unique_id})
               elif message.text:                 
                   # Learning: word (text/sticker ID) -> text (text)
                   chat_collection.insert_one({"word": word_to_learn, "text": message.text, "check": "none"})
                   
       # Bot is the one replying (Autoreply Logic)
       elif message.reply_to_message.from_user.id == bot_id: 
           if not is_v:                   
               await bot.send_chat_action(message.chat.id, "typing")
               word = message.text if message.text else message.sticker.file_unique_id
               reply, Yo = await get_ai_response(word)
               
               if reply:
                   if Yo == "sticker":
                       await message.reply_sticker(reply)
                   else: # Yo == "none" or "text"
                       await message.reply_text(reply)


# Note: The original code had two separate handlers (vai and vstickerai) for text-only 
# and sticker-only triggers, but the logic was almost identical and handled both 
# in each. I've merged the core autoreply/learning logic into one handler (vai) 
# for cleaner separation, covering text and sticker inputs for both 'word' and 'text'.


# --- Private Chat Logic ---

@bot.on_message(
    (
        filters.text
        | filters.sticker
    )
    & filters.private
    & ~filters.bot,
)
async def vprivate(client: Client, message: Message):
   
    # Determine the 'word' for the search
    word_to_search = message.text if message.text else message.sticker.file_unique_id

    # The original private chat logic only searched based on the incoming message, 
    # regardless of whether it was a reply to the bot or not.
    # It also didn't include the learning feature in private chat.
    
    await bot.send_chat_action(message.chat.id, "typing")
    reply, Yo = await get_ai_response(word_to_search)

    if reply:
        if Yo == "sticker":
            await message.reply_sticker(reply)
        elif Yo == "text" or Yo == "none":
            await message.reply_text(reply)


if __name__ == "__main__":
    print("Bot is starting...")
    bot.run()

