# Automatically set the file type to video
if file.media in [MessageMediaType.VIDEO, MessageMediaType.DOCUMENT, MessageMediaType.AUDIO]:
    await message.reply_text(
        f"**Processing file as video.**\n**• File Name :-**```{new_name}```",
        reply_to_message_id=file.id,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🚀 Uploading as Video", callback_data="upload_video")]])
    )