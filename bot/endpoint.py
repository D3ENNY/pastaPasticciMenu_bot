from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/first_test', methods=['GET'])
def first_test():
    return jsonify({
        "message": "Hello World!"
    })

if __name__ == '__main__':
    app.run(debug=True)