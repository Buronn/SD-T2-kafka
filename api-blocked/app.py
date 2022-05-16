from flask import Flask, jsonify, request

from db.config import Config
app = Flask(__name__)
app.config.from_object(Config)

@app.route('/blocked', methods=['GET'])
def blocked():
    print("blockeado cabron")
    return jsonify({'blocked': True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
