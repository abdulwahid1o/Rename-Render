from pyrogram import Client, filters
from helper.database import db
import os
from moviepy.editor import VideoFileClip

# Initialize the bot
app = Client("my_bot")

# Function to extract a thumbnail from a video
def extract_thumbnail(video_path, thumbnail_path, time=1.0):
    """Extract a thumbnail from the video at the given time (in seconds)."""
    with VideoFileClip(video_path) as video:
        video.save_frame(thumbnail_path, t=time)

# Command to view the saved thumbnail
@app.on_message(filters.private & filters.command(['viewthumb']))
async def viewthumb(client, message):    
    thumb = await db.get_thumbnail(message.from_user.id)
    if thumb:
        await client.send_photo(
            chat_id=message.chat.id, 
            photo=thumb
        )
    else:
        await message.reply_text("😔**Sorry! No thumbnail found...**😔") 

# Command to delete the saved thumbnail
@app.on_message(filters.private & filters.command(['delthumb']))
async def removethumb(client, message):
    await db.set_thumbnail(message.from_user.id, file_id=None)
    await message.reply_text("**Thumbnail deleted successfully**✅️")

# Command to save a new thumbnail
@app.on_message(filters.private & filters.photo)
async def addthumbs(client, message):
    lazy_dev = await message.reply_text("Please Wait ...")
    await db.set_thumbnail(message.from_user.id, file_id=message.photo.file_id)                
    await lazy_dev.edit("**Thumbnail saved successfully**✅️")

# Automatically extract and set a thumbnail when a video is uploaded
@app.on_message(filters.video)
async def handle_video(client, message):
    video = message.video
    video_path = await message.download()

    # Define the path for the thumbnail
    thumbnail_path = f"{os.path.splitext(video_path)[0]}_thumbnail.jpg"
    
    # Extract thumbnail from the video
    extract_thumbnail(video_path, thumbnail_path)
    
    # Send the video with the automatically generated thumbnail
    await message.reply_video(video=video_path, thumb=thumbnail_path)

    # Optionally, remove the downloaded video and thumbnail to save space
    os.remove(video_path)
    os.remove(thumbnail_path)

# Start the bot
app.run()
