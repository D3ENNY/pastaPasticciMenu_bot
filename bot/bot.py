from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler  
import json, asyncio, traceback

# Load JSON
with open("./config/config.json", 'r') as config:
    bot_config = json.load(config)

class TgBot:
    
    def __init__(self):
        """Inizializzazione del bot"""
        self.app = Client(
                        bot_config["description"],
                        api_id = bot_config["api_id"],
                        api_hash = bot_config["api_hash"],
                        bot_token = bot_config["bot_token"]
                    )
    
    async def start_bot(self):
        """Avvia il bot e verifica se è correttamente connesso"""
        await self.app.start() 
        
        if self.app.me:
            print(f"Bot is logged in as: {self.app.me.first_name}")
        else:
            print("Bot failed to login.")
            
        
    async def send_message_async(self, chat_id, photo, desc):
        """Manda il menu ad una chat"""
        print(f"Sending message to {chat_id} with description: {desc}")
        
        try:
            if photo:

                print(f"Sending photo with size: {len(photo.getvalue())} bytes")
                await self.app.send_photo(chat_id, photo, caption=desc)
            else:
                await self.app.send_message(chat_id, desc)
        except Exception as e:
            print(f"Error sending message: {e}")
            #traceback.print_exc()
