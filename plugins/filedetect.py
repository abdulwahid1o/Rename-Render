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
               extn = "mp4"  # Default extension set to .mp4 for videos
           new_name = new_name + "." + extn

       await reply_message.delete()

       # Automatically send the file as a video
       await client.send_message(
           chat_id=message.chat.id,
           text=f"Processing file as video: **{new_name}**",
           reply_to_message_id=file.id
       )
       await client.send_video(
           chat_id=message.chat.id,
           video=file.file_id,
           caption=f"**{new_name}**"
       )