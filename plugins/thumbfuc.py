import pyrogram
from pyrogram import filters

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
app = pyrogram.Client('my_bot', bot_token='7514260749:AAHib0PGo8F-DqF6IG9KPAoKUqvvA1OXN24')

@app.on_message(filters.video)
async def add_thumbnail(client, message):
    # Get the video file ID
    video_file_id = message.video.file_id

    # Download the video to a temporary file
    video_path = await client.download_media(video_file_id, file_name='video.mp4')

    # Extract the thumbnail at the 15-second mark using FFmpeg
    thumbnail_path = 'thumbnail.jpg'
    result = await client.run_inline_query(
        'ffmpeg',
        f'ss=15 t=0.01 -i {video_path} -vf scale=-1:240 -an {thumbnail_path}'
    )
    photo_file_id = result.results[0].document.file_id

    # Download the thumbnail
    thumbnail_path = await client.download_media(photo_file_id, file_name='thumbnail.jpg')

    # Add the thumbnail to the beginning of the video using FFmpeg
    output_video_path = 'output_video.mp4'
    result = await client.run_inline_query(
        'ffmpeg',
        f'-i {video_path} -i {thumbnail_path} -filter_complex overlay=x=0:y=0 {output_video_path}'
    )

    # Send the modified video to the user
    await client.send_video(message.chat.id, output_video_path)

if __name__ == '__main__':
    app.run()
