from flask import Flask, jsonify, request

from db.models import User
from db.models import db
from db.models import to_dict
from db.config import Config
from functions import register_check
from kafka import KafkaProducer
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
        db.session.add(user)
        db.session.commit()

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data received'}), 400
    if not data.get('user') or not data.get('password'):
        return jsonify({'error': 'Missing data'}), 400
    user = User.query.filter_by(user=data['user']).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    if not bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
        return jsonify({'error': 'Wrong password'}), 401
    return jsonify({'user': user.user, 'id': user.id}), 200


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    print("data:", data)
    answer = register_check(data)
    return answer
@app.route('/usuarios', methods=['GET','DELETE'])
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
