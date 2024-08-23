from pyrogram import Client, filters
from helper.database import db
import subprocess

@Client.on_message(filters.private & filters.command(['viewthumb']))
async def viewthumb(client, message):    
    thumb = await db.get_thumbnail(message.from_user.id)
    if thumb:
       await client.send_photo(
           chat_id=message.chat.id, 
           photo=thumb)
    else:
        await message.reply_text("😔**Sorry ! No thumbnail found...**😔") 

@Client.on_message(filters.private & filters.command(['delthumb']))
async def removethumb(client, message):
    await db.set_thumbnail(message.from_user.id, file_id=None)
    await message.reply_text("**Thumbnail deleted successfully**✅️")

@Client.on_message(filters.private & filters.video)
async def addthumbs(client, message):
    video_path = await message.download() # Download the video
    thumb_path = extract_thumbnail(video_path) # Extract the thumbnail
    LazyDev = await message.reply_text("Please Wait ...")
    await db.set_thumbnail(message.from_user.id, file_id=thumb_path)                
    await LazyDev.edit("**Thumbnail saved successfully**✅️")

def extract_thumbnail(video_path):
    thumb_path = video_path.replace('.mp4', '_thumb.jpg')
    command = [
        'ffmpeg', '-i', video_path, '-ss', '00:00:15.000', '-vframes', '1', thumb_path
    ]
    subprocess.run(command, check=True)
    return thumb_path