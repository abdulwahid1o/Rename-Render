from pyrogram import Client, filters
from pyrogram.enums import MessageMediaType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply

@Client.on_message(filters.private & filters.reply)
async def refunc(client, message):
    reply_message = message.reply_to_message
    if reply_message.reply_markup and isinstance(reply_message.reply_markup, ForceReply):
        new_name = message.text
        await message.delete()
        msg = await client.get_messages(message.chat.id, reply_message.id)
        file = msg.reply_to_message
        media = getattr(file, file.media.value)

        # Ensure the file has an appropriate extension
        if not "." in new_name:
            extn = media.file_name.rsplit('.', 1)[-1] if "." in media.file_name else "mp4"
            new_name = new_name + "." + extn
        await reply_message.delete()

        # Automatically set the button to convert to video
        button = [[InlineKeyboardButton("🎥 Convert to Video", callback_data="upload_video")]]

        # Adding document and audio options in case they are still needed
        if file.media == MessageMediaType.DOCUMENT:
            button.append([InlineKeyboardButton("📁 Keep as Document", callback_data="upload_document")])
        elif file.media == MessageMediaType.AUDIO:
            button.append([InlineKeyboardButton("🎵 Convert to Audio", callback_data="upload_audio")])

        await message.reply_text(
            f"**File will be converted to video by default.**\n**• File Name :-** ```{new_name}```",
            reply_to_message_id=file.id,
            reply_markup=InlineKeyboardMarkup(button)
        )