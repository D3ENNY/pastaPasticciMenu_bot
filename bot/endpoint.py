import os, base64, asyncio, io, threading
from flask import Flask, jsonify, request

from bot import TgBot

app = Flask(__name__)
bot = TgBot()

loop = asyncio.get_event_loop()

def start_bot():
    loop.run_until_complete(bot.start_bot())


@app.route('/api/first_test', methods=['GET'])
def first_test():
    return jsonify({
        "message": "Hello World!"
    })

@app.route('/api/upload_menu', methods=['POST'])
def receive_menu():
    try:
        json = request.get_json()
        
        if not json: 
            return jsonify({
                "error": "No JSON data received. Please send a valid JSON request."
            }), 400

        image_base64 = json.get("menu_base64")
        if not image_base64:
            return jsonify({
                "error": "Missing 'menu_base64' field in the request body."
            }), 400
            
        image_bytes = base64.b64decode(image_base64)
        image_binary = io.BytesIO(image_bytes)

        with open(os.path.join("uploads", "output.png"), "wb") as output: 
            output.write(image_bytes)

        # Avvia la funzione asincrona in un nuovo thread separato
        loop.run_until_complete(bot.send_message_async(-2229775701, image_binary, "menu del giorno"))
        
        return jsonify({
            "message": "Image successfully received!", 
            "file_path": os.path.join("uploads", "output.png")
        })
        
    except Exception as ex:
        return jsonify({
            "error": f"An error occurred:\n{str(ex)}"
        }), 500


def send_async_message(bot, chat_id, message, photo=None):
    """Funzione separata per inviare il messaggio in modo asincrono"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(bot.send_message_async(chat_id, message, photo))

if __name__ == '__main__':
    bot_thread = threading.Thread(target=start_bot)
    bot_thread.start()
    
    app.run(debug=True, use_reloader=False) 