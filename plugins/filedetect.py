
from pyrogram import Client, filters
from pyrogram.enums import MessageMediaType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply

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

       button = [[InlineKeyboardButton("📁 𝙳𝙾𝙲𝚄𝙼𝙴𝙽𝚃𝚂",callback_data = "upload_document")]]
       if file.media in [MessageMediaType.VIDEO, MessageMediaType.DOCUMENT]:
           button.append([InlineKeyboardButton("🎥 𝚅𝙸𝙳𝙴𝙾",callback_data = "upload_video")])
       elif file.media == MessageMediaType.AUDIO:
           button.append([InlineKeyboardButton("🎵 𝙰𝙾𝚄𝙳𝙸𝙾",callback_data = "upload_audio")])
       await message.reply_text(
          f"**Select the output file type**\n**• File Name :-**```{new_name}```",
          reply_to_message_id=file.id,
          reply_markup=InlineKeyboardMarkup(button))



import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from helper.utility import extract_thumbnail

@Client.on_message(filters.video)
async def handle_video_message(client, message):
    video_file = await message.download()  # Download the video
    thumbnail_file = video_file.replace('.mp4', '_thumb.jpg')  # Define the thumbnail path

    try:
        await extract_thumbnail(video_file, thumbnail_file, time="00:00:01")
        # You can now send the thumbnail, e.g., as a reply to the message:
        await message.reply_photo(thumbnail_file, caption="Here's your thumbnail!")
    except FloodWait as e:
        print(f"FloodWait exception occurred: Waiting for {e.x} seconds")
        await asyncio.sleep(e.x)  # Wait for the specified time
        await handle_video_message(client, message)  # Retry the operation