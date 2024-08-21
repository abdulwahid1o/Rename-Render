from pyrogram import Client, filters
from helper.database import db

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
	
@Client.on_message(filters.private & filters.photo)
async def addthumbs(client, message):
    AbdulWahid = await message.reply_text("Please Wait ...")
    await db.set_thumbnail(message.from_user.id, file_id=message.photo.file_id)                
    await AbdulWahid.edit("**Thumbnail saved successfully**✅️")



import os
import ffmpeg
from pyrogram import Client, filters
from pyrogram.types import InputMediaPhoto

app = Client("my_bot")

# Function to extract thumbnail
def extract_thumbnail(video_path, thumbnail_path, time='00:00:01'):
    try:
        (
            ffmpeg
            .input(video_path, ss=time)
            .filter('scale', 320, -1)
            .output(thumbnail_path, vframes=1)
            .run()
        )
    except Exception as e:
        print(f"Error extracting thumbnail: {e}")

@app.on_message(filters.video)
async def video_handler(client, message):
    video = await message.download()
    thumbnail_path = f"{os.path.splitext(video)[0]}_thumbnail.jpg"

    # Extract thumbnail
    extract_thumbnail(video, thumbnail_path)

    # Send the video with the thumbnail
    await message.reply_video(
        video,
        thumb=thumbnail_path,
        caption="Here is your video with an auto-generated thumbnail!"
    )

    # Clean up
    os.remove(video)
    os.remove(thumbnail_path)
