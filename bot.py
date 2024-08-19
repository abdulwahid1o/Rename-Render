# Don't Remove Credit @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01

import logging
import logging.config
from pyrogram import Client, errors
from config import API_ID, API_HASH, BOT_TOKEN, FORCE_SUB, PORT
from aiohttp import web
from plugins.web_support import web_server
import asyncio

logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)


class Bot(Client):

    def __init__(self):
        super().__init__(
            name="WebX-Renamer",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=50,
            plugins={"root": "plugins"},
            sleep_threshold=5,
        )

    async def start(self):
        retries = 5
        for attempt in range(retries):
            try:
                await super().start()
                break
            except errors.BadMsgNotification as e:
                logging.warning(f"Attempt {attempt + 1} failed with error: {e}. Retrying in 5 seconds...")
                await asyncio.sleep(5)
        else:
            logging.error("Failed to synchronize time after several attempts. Exiting.")
            return

        me = await self.get_me()
        self.mention = me.mention
        self.username = me.username 
        self.force_channel = FORCE_SUB
        if FORCE_SUB:
            try:
                link = await self.export_chat_invite_link(FORCE_SUB)                  
                self.invitelink = link
            except Exception as e:
                logging.warning(e)
                logging.warning("Make Sure Bot admin in force sub channel")             
                self.force_channel = None
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, PORT).start()
        logging.info(f"{me.first_name} ✅✅ BOT started successfully ✅✅")
      

    async def stop(self, *args):
        await super().stop()      
        logging.info("Bot Stopped 🙄")
        
bot = Bot()
bot.run()