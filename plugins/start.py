from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import humanize
from helper.database import db
from cb_data import upload  # Importing the upload function from cb_data.py
from config import START_PIC, ADMIN 

@Client.on_message(filters.private & filters.command(["start"]))
async def start(client, message):
    user = message.from_user
    if not await db.is_user_exist(user.id):
        await db.add_user(user.id)             
    txt=f"👋 Hello Developer {user.mention} \n\nI am an Advanced file Renamer and file Converter BOT with Custom thumbnail support.\n\nSend me any video or document !"
    button=InlineKeyboardMarkup([[
        InlineKeyboardButton(" Developer ", url='https://t.me/anjel_neha')
        ],[
        InlineKeyboardButton(' Updates', url='https://t.me/VJ_Bots'),
        InlineKeyboardButton(' Support', url='https://t.me/vj_bot_disscussion')
        ],[
        InlineKeyboardButton(' About', callback_data='about'),
        InlineKeyboardButton(' Help', callback_data='help')
        ],[
        InlineKeyboardButton(" Join Our Movie Channel !", url='https://t.me/VJ_Bots')
        ],[
        InlineKeyboardButton("❤️ Subscribe YT ❤️", url='https://www.youtube.com/@Tech_VJ')
        ]
        ])
    if START_PIC:
        await message.reply_photo(START_PIC, caption=txt, reply_markup=button)       
    else:
        await message.reply_text(text=txt, reply_markup=button, disable_web_page_preview=True)

@Client.on_message(filters.command('logs') & filters.user(ADMIN))
async def log_file(client, message):
    try:
        await message.reply_document('TelegramBot.log')
    except Exception as e:
        await message.reply_text(f"Error:\n`{e}`")

@Client.on_message(filters.private & (filters.document | filters.video))
async def rename_start(client, message):
    file = getattr(message, message.media.value)
    filename = file.file_name
    filesize = humanize.naturalsize(file.file_size) 
    fileid = file.file_id

    text = f"""**__File received__**\n\n**File Name** :- `{filename}`\n**File Size** :- `{filesize}`\n\n__Processing...__"""
    await message.reply_text(text=text, reply_to_message_id=message.id)

    # Trigger the upload process directly
    await upload(client, message)  # Directly calling the upload function