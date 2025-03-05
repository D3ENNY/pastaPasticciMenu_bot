from flask import Flask, jsonify, request
import base64, os

from bot import TgBot

app = Flask(__name__)
bot = TgBot()

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
        
        #solo per test
        with open(os.path.join("uploads", "output.png"), "wb") as output: 
            output.write(image_bytes)
        
        return jsonify({
            "message": "image succesfully received!", 
            "file_path": os.path.join("uploads", "output.png")
        })
        
        
    except Exception as ex:
        return jsonify({
            "error": f"An error occurred:\n{str(ex)}"
        }), 500

if __name__ == '__main__':
    app.run(debug=True)