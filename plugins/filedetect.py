import os
import time
from PIL import Image
from pyrogram import Client, filters
from pyrogram.types import ForceReply
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from helper.progress import progress_for_pyrogram
from helper.tools import convert
from database.db import db

@Client.on_message(filters.private & filters.reply)
async def refunc(client, message):
    reply_message = message.reply_to_message
    if reply_message.reply_markup and isinstance(reply_message.reply_markup, ForceReply):
        await message.delete()
        msg = await client.get_messages(message.chat.id, reply_message.id)
        file = msg.reply_to_message
        media = getattr(file, file.media.value)

        # Automatically generate the new file name
        new_name = media.file_name
        if not "." in new_name:
            extn = media.file_name.rsplit('.', 1)[-1] if "." in media.file_name else "mkv"
            new_name = new_name + "." + extn

        # Directly proceed with the conversion without asking for the file type
        await upload_file(client, file, new_name)

async def upload_file(client, file, new_name):
    ms = await file.reply_text("⚠️__**Please wait...**__\n__Downloading file to my server...__")
    c_time = time.time()
    try:
        path = await client.download_media(
            message=file, 
            progress=progress_for_pyrogram,
            progress_args=("\n⚠️__**Please wait...**__\n\n😈 **Video Converter Bot in progress...**", ms, c_time)
        )
    except Exception as e:
        await ms.edit(str(e))
        return 

    file_path = path  # Use the original path as the file_path
    duration = 0
    try:
        metadata = extractMetadata(createParser(file_path))
        if metadata.has("duration"):
            duration = metadata.get('duration').seconds
    except:
        pass

    user_id = int(file.chat.id)
    ph_path = None
    media = getattr(file, file.media.value)
    c_caption = await db.get_caption(file.chat.id)
    c_thumb = await db.get_thumbnail(file.chat.id)

    caption = c_caption.format(
        filename=os.path.basename(file_path), 
        filesize=humanize.naturalsize(media.file_size), 
        duration=convert(duration)
    ) if c_caption else f"**{os.path.basename(file_path)}**"

    if media.thumbs or c_thumb:
        ph_path = await client.download_media(c_thumb) if c_thumb else await client.download_media(media.thumbs[0].file_id)
        Image.open(ph_path).convert("RGB").save(ph_path)
        img = Image.open(ph_path)
        img.resize((320, 320))
        img.save(ph_path, "JPEG")

    await ms.edit("⚠️__**Please wait...**__\n__Processing file upload....__")
    c_time = time.time()

    try:
        await client.send_video(
            file.chat.id,
            video=file_path,
            caption=caption,
            thumb=ph_path,
            duration=duration,
            progress=progress_for_pyrogram,
            progress_args=("⚠️__**Please wait...**__\n__Processing file upload....__", ms, c_time)
        )
    except Exception as e:
        await ms.edit(f"Error: {e}")
        os.remove(file_path)
        if ph_path:
            os.remove(ph_path)
        return

    await ms.delete()
    os.remove(file_path)
    if ph_path:
        os.remove(ph_path)