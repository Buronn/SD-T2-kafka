import json
from flask import Flask, jsonify, request
from db.config import Config

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/blocked', methods=['GET'])
def blocked():
    with open('data.txt', 'r') as f:
        data = f.read()
        f.close()
    data = data.split('\n')
    data = list(filter(None, data))
    
    return jsonify({'data': data})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
