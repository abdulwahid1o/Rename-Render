from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
import json

# Assuming preferences are stored in a JSON file
PREFERENCES_FILE = "preferences.json"

# Load preferences from file
def load_preferences():
    if os.path.exists(PREFERENCES_FILE):
        with open(PREFERENCES_FILE, "r") as f:
            return json.load(f)
    return {}

# Save preferences to file
def save_preferences(preferences):
    with open(PREFERENCES_FILE, "w") as f:
        json.dump(preferences, f, indent=4)

# Set media preference command
@Client.on_message(filters.private & filters.command("setmedia"))
async def set_media_command(client, message):
    user_id = str(message.from_user.id)
    media_type = message.text.split("/setmedia", 1)[1].strip().lower()

    if media_type not in ["video", "document"]:
        await message.reply_text(f"**Invalid media type! Please choose 'video' or 'document'.**")
        return

    preferences = load_preferences()
    preferences[user_id] = media_type
    save_preferences(preferences)

    await message.reply_text(f"**Media Preference Set To :** {media_type} ✅", reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("🗑️ Delete Preference", callback_data=f"delete_{user_id}")]
    ]))

# Handle callback queries
@Client.on_callback_query(filters.regex(r"delete_\d+"))
async def delete_preference(client, callback_query):
    user_id = callback_query.data.split("_")[1]
    preferences = load_preferences()

    if user_id in preferences:
        del preferences[user_id]
        save_preferences(preferences)
        await callback_query.message.edit_text("**Media preference deleted successfully.**")
    else:
        await callback_query.message.edit_text("**No preference set to delete.**")

# Get media preference function
def get_media_preference(user_id):
    preferences = load_preferences()
    return preferences.get(str(user_id), None)
