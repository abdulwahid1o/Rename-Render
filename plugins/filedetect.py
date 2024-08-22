from pyrogram import Client, filters
from pyrogram.enums import MessageMediaType
from pyrogram.types import ForceReply

@Client.on_message(filters.private & filters.reply)
async def refunc(client, message):
    reply_message = message.reply_to_message
    if (reply_message.reply_markup) and isinstance(reply_message.reply_markup, ForceReply):
        new_name = message.text
        await message.delete()
        msg = await client.get_messages(message.chat.id, reply_message.id)
        file = msg.reply_to_message
        media = getattr(file, file.media.value)
        
        if not "." in new_name:
            if "." in media.file_name:
                extn = media.file_name.rsplit('.', 1)[-1]
            else:
                extn = "mkv"
            new_name = new_name + "." + extn
        
        await reply_message.delete()

        try:
            if file.media == MessageMediaType.VIDEO:
                # If the file is a video, send it as a video
                await client.send_video(
                    chat_id=message.chat.id,
                    video=media.file_id,
                    caption=f"**File renamed to:** `{new_name}`",
                    file_name=new_name,
                    supports_streaming=True,
                    reply_to_message_id=file.id
                )
            elif file.media == MessageMediaType.DOCUMENT:
                # If the file is a document, resend it as a document with a new name
                await client.send_document(
                    chat_id=message.chat.id,
                    document=media.file_id,
                    caption=f"**File renamed to:** `{new_name}`",
                    file_name=new_name,
                    reply_to_message_id=file.id
                )
            else:
                await message.reply_text("This file type is not supported for automatic video conversion.")
        except Exception as e:
            await message.reply_text(f"An error occurred: {str(e)}")
            
            
            import os
import subprocess
from pyrogram import Client, filters
from pyrogram.enums import MessageMediaType
from pyrogram.types import ForceReply

@Client.on_message(filters.private & filters.reply)
async def refunc(client, message):
    reply_message = message.reply_to_message
    if (reply_message.reply_markup) and isinstance(reply_message.reply_markup, ForceReply):
        new_name = message.text
        await message.delete()
        msg