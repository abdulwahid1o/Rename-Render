import cv2
import telebot
import ffmpeg

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot = telebot.TeleBot('YOUR_BOT_TOKEN')

@bot.message_handler(content_types=['video'])
def handle_video(message):
    # Get the video file ID
    video_file_id = message.video.file_id

    # Download the video file
    file_path = bot.download_file(video_file_id)

    # Extract the thumbnail at the 15-second mark
    thumbnail_path = "thumbnail.jpg"
    ffmpeg.input(file_path).output(thumbnail_path, ss=15, t=0.01).run()

    # Add the thumbnail to the video at the beginning
    output_video_path = "output_video.mp4"
    ffmpeg.input(file_path).complex_filter("overlay=x=0:y=0[out0]").output(output_video_path).run()

    # Send the output video to the user
    with open(output_video_path, 'rb') as video:
        bot.send_video(message.chat.id, video)

# Start the bot
bot.polling()
