from flask import Flask, jsonify, request

from db.models import User
from db.models import db
from db.models import to_dict
from db.config import Config
from functions import register_check
import os
import bcrypt
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
db.create_all(app=app)
with app.app_context():
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw('pass123'.encode('utf-8'), salt)
    if not User or not User.query.first():
        user = User(
            user='user',
            password=hashed_password.decode('utf-8'),
        )



@app.route('/')
def hello_world():
    return 'Hello, World!'
@app.route('/api/v1/register', methods=['POST'])
def register():
    data = request.get_json()
    print("data:", data)
    answer = register_check(data)
    return answer
@app.route('/api/v1/usuarios', methods=['GET','DELETE'])
def get_body():
    if request.method == 'GET':
        if request.args.get('id'):
            user = User.query.filter_by(id=request.args.get('id')).first()
            if user:
                return jsonify(to_dict(user))
            else:
                return jsonify({"error": "User not found"}), 404
        else:
            users = User.query.all()
            return jsonify([to_dict(user) for user in users])
    elif request.method == 'DELETE':
        if request.args.get('id'):
            user = User.query.filter_by(id=request.args.get('id')).first()
            if user:
                user_name = user.name
                db.session.delete(user)
                db.session.commit()
                return jsonify({"message": "User "+user_name+" deleted"}), 200
            else:
                return jsonify({"error": "User not found"}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
