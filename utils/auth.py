from flask import request, jsonify
from flask_jwt_extended import create_access_token
from models import db, User
from utils.security import validate_input

def signup():
    phone_number = validate_input(request.json.get('phone_number', None))
    password = validate_input(request.json.get('password', None))
    
    if User.query.filter_by(phone_number=phone_number).first():
        return jsonify({"msg": "User already exists"}), 400

    user = User(phone_number=phone_number)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"msg": "User created successfully"}), 201

def login():
    phone_number = validate_input(request.json.get('phone_number', None))
    password = validate_input(request.json.get('password', None))
    user = User.query.filter_by(phone_number=phone_number).first()

    if user is None or not user.check_password(password):
        return jsonify({"msg": "Bad phone number or password"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token), 200