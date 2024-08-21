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



import ffmpeg
import os

def extract_thumbnail(video_path, thumbnail_path, time="00:00:01"):
    """
    Extracts a thumbnail from the video at a specific time.
    
    :param video_path: Path to the input video file.
    :param thumbnail_path: Path where the thumbnail image will be saved.
    :param time: The timestamp in the video to capture the thumbnail (format: HH:MM:SS).
    :return: None
    """
    try:
        (
            ffmpeg
            .input(video_path, ss=time)
            .filter('scale', 320, -1)
            .output(thumbnail_path, vframes=1)
            .run(overwrite_output=True)
        )
        print(f"Thumbnail saved to {thumbnail_path}")
    except ffmpeg.Error as e:
        print(f"Error extracting thumbnail: {e.stderr.decode()}")

# Example Usage
video_file = 'path_to_your_video.mp4'
thumbnail_file = 'path_to_save_thumbnail.jpg'

# Extract thumbnail at 1 second
extract_thumbnail(video_file, thumbnail_file, time="00:00:01")
