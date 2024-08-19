@Client.on_callback_query(filters.regex("upload"))
async def upload(bot, update):
    file = update.message.reply_to_message
    ms = await update.message.edit("⚠️__**Please wait...**__\n__Downloading file to my server...__")
    c_time = time.time()

    try:
        path = await bot.download_media(
            message=file, 
            progress=progress_for_pyrogram,
            progress_args=("\n⚠️__**Please wait...**__\n\n😈 **Video Converter Bot in progress...**",  ms, c_time)
        )
    except Exception as e:
        await ms.edit(str(e))
        return 

    file_path = path
    duration = 0
    try:
        metadata = extractMetadata(createParser(file_path))
        if metadata.has("duration"):
            duration = metadata.get('duration').seconds
    except:
        pass

    user_id = int(update.message.chat.id)
    ph_path = None
    media = getattr(file, file.media.value)
    c_caption = await db.get_caption(update.message.chat.id)
    c_thumb = await db.get_thumbnail(update.message.chat.id)

    caption = c_caption.format(
        filename=os.path.basename(file_path), 
        filesize=humanize.naturalsize(media.file_size), 
        duration=convert(duration)
    ) if c_caption else f"**{os.path.basename(file_path)}**"

    if media.thumbs or c_thumb:
        ph_path = await bot.download_media(c_thumb) if c_thumb else await bot.download_media(media.thumbs[0].file_id)
        Image.open(ph_path).convert("RGB").save(ph_path)
        img = Image.open(ph_path)
        img.resize((320, 320))
        img.save(ph_path, "JPEG")

    await ms.edit("⚠️__**Please wait...**__\n__Processing file upload....__")
    c_time = time.time()

    try:
        await bot.send_video(
            update.message.chat.id,
            video=file_path,
            caption=caption,
            thumb=ph_path,
            duration=duration,
            progress=progress_for_pyrogram,
            progress_args=("⚠️__**Please wait...**__\n__Processing file upload....__", ms, c_time)
        )
    except Exception as e:
        await ms.edit(f"Error: {e}")
        os.remove(file_path)
        if ph_path:
            os.remove(ph_path)
        return

    await ms.delete()
    os.remove(file_path)
    if ph_path:
        os.remove(ph_path)