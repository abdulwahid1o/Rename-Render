from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Assume that the database methods are in a helper file `database.py`
from helper.database import set_media_preference, get_media_preference, delete_media_preference

@Client.on_message(filters.private & filters.command("setmedia"))
async def set_media_command(client, message):
    user_id = message.from_user.id    
    media_type = message.text.split("/setmedia", 1)[1].strip().lower()

    if media_type not in ["video", "document"]:
        await message.reply_text("**Invalid media type! Please use 'video' or 'document'.**")
        return

    # Save the preferred media type to the database
    await set_media_preference(user_id, media_type)

    await message.reply_text(f"**Media Preference Set To:** {media_type} ✅")

@Client.on_message(filters.private & filters.command("getmedia"))
async def get_media_command(client, message):
    user_id = message.from_user.id    
    media_type = await get_media_preference(user_id)

    if media_type:
        await message.reply_text(f"**Current Media Preference:** {media_type}")
    else:
        await message.reply_text("**No media preference set!**")

@Client.on_message(filters.private & filters.command("delmedia"))
async def del_media_command(client, message):
    user_id = message.from_user.id

    # Delete the media preference
    await delete_media_preference(user_id)

    await message.reply_text("**Media Preference Deleted! You can set it again using /setmedia.**")
