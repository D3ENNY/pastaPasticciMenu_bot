import base64, os
from flask import Flask, jsonify, request

app = Flask(__name__)

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
                "error": "No data sent to request"
            }), 400

        image_base64 = json.get("menu_base64")
        if not image_base64:
            return jsonify({
                "error": "expected menu_base64 data but no data sent"
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
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)