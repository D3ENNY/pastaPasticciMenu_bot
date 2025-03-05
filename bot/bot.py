from pyrogram import Client
import json, asyncio


#load JSON
with open("./config/config.json", 'r') as config:
    bot_config = json.load(config)

class TgBot:
    
    def __init__(self):
        """inizializzazione del bot"""
        self.app = Client(
                        bot_config["description"],
                        api_id = bot_config["api_id"],
                        api_hash = bot_config["api_hash"],
                        bot_token = bot_config["bot_token"]
                    )
    
    async def send_message_async(self, chat_id, photo, desc):
        """manda il menu ad una chat"""
        async with self.app:
            await self.app.send_photo(chat_id, photo, caption=desc)
            
        async def send_message_async(self, chat_id, message):
            """manda un messaggio ad una chat"""
            async with self.app:
                await self.app.send_message(chat_id, message)
    
    def send_message(self, chat_id, message, photo=None):
        """Funzione pubblica per mandare un messaggio"""
        if not photo:
            asyncio.run(self.send_message_async(chat_id=chat_id, message=message))
        else:
            asyncio.run(self.send_message_async(chat_id=chat_id, photo=photo, desc=message))