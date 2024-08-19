from asyncio import sleep
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply, CallbackQuery
from pyrogram.errors import FloodWait
import humanize
import random
from helper.txt import mr
from helper.database import db
from config import START_PIC, FLOOD, ADMIN
import time
import os

@Client.on_message(filters.private & filters.command(["start"]))
async def start(client, message):
    user = message.from_user
    if not await db.is_user_exist(user.id):
        await db.add_user(user.id)             
    txt = f"👋 Hello Developer {user.mention} \n\nI am an Advance file Renamer and file Converter BOT with Custom thumbnail support.\n\nSend me any video or document!"
    button = InlineKeyboardMarkup([[
        InlineKeyboardButton(' About', callback_data='about'),
        InlineKeyboardButton(' Help', callback_data='help')
    ]])
    if START_PIC:
        await message.reply_photo(START_PIC, caption=txt, reply_markup=button)
    else:
        await message.reply_text(text=txt, reply_markup=button, disable_web_page_preview=True)

@Client.on_message(filters.command('logs') & filters.user(ADMIN))
async def log_file(client, message):
    try:
        await message.reply_document('TelegramBot.log')
    except Exception as e:
        await message.reply_text(f"Error:\n`{e}`")

@Client.on_message(filters.private & (filters.document | filters.audio | filters.video))
async def rename_start(client, message):
    file = getattr(message, message.media.value)
    filename = file.file_name
    filesize = humanize.naturalsize(file.file_size)
    fileid = file.file_id

    # Inform user that the processing has started
    text = f"**Processing the file:** `{filename}`\n**File Size:** `{filesize}`"
    await message.reply_text(text=text, reply_to_message_id=message.id)

    # Call the file conversion function
    await process_file_conversion(client, message, fileid, filename)

async def process_file_conversion(client, message, fileid, filename):
    try:
        # Download the file
        file_path = await client.download_media(fileid)
        
        # Convert the file (if needed) and prepare for upload
        # Replace this with your actual conversion process if any
        # Assuming the file is already in the correct format and just needs uploading
        
        duration = 0
        ph_path = None  # Thumbnail path
        # Extract metadata if needed (e.g., duration)
        # If needed, insert your metadata extraction logic here
        
        # Use default caption if no custom caption is set
        caption = f"**{filename}**"
        
        # Send the file as a video
        await client.send_video(
            chat_id=message.chat.id,
            video=file_path,
            caption=caption,
            duration=duration,
            thumb=ph_path
        )

        # Cleanup
        os.remove(file_path)
        if ph_path:
            os.remove(ph_path)

    except Exception as e:
        await message.reply_text(f"Error during file processing: {str(e)}")

@Client.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    data = query.data
    if data == "start":
        await query.message.edit_text(
            text=f"""👋 Hello Developer {query.from_user.mention} \n\nI am an Advance file Renamer and file Converter BOT with permanent and custom thumbnail support.\n\nSend me any video or document!""",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(' About', callback_data='about'),
                InlineKeyboardButton(' Help', callback_data='help')
            ]])
        )
    elif data == "help":
        await query.message.edit_text(
            text=mr.HELP_TXT,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(" Join our Channel ", url="https://t.me/abdul_wahid101")
            ], [
                InlineKeyboardButton(" 𝙲𝙻𝙾𝚂𝙴", callback_data="close"),
                InlineKeyboardButton(" 𝙱𝙰𝙲𝙺", callback_data="start")
            ]])
        )
    elif data == "about":
        await query.message.edit_text(
            text=mr.ABOUT_TXT.format(client.mention),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(" Join our Channel ", url="https://t.me/abdul_wahid101")
            ], [
                InlineKeyboardButton(" 𝙲𝙻𝙾𝚂𝙴", callback_data="close"),
                InlineKeyboardButton(" 𝙱𝙰𝙲𝙺", callback_data="start")
            ]])
        )
    elif data == "dev":
        await query.message.edit_text(
            text=mr.DEV_TXT,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(" Join our Channel ", url="https://t.me/abdul_wahid101")
            ], [
                InlineKeyboardButton(" 𝙲𝙻𝙾𝚂𝙴", callback_data="close"),
                InlineKeyboardButton(" 𝙱𝙰𝙲𝙺", callback_data="start")
            ]])
        )
    elif data == "close":
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
        except:
            await query.message.delete()