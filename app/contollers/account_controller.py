from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.extensions import db
from app.models.user import User
from app.models.wallet import Wallet
from app.services.binance_service import BinanceService

def signup():
    data = request.get_json()
    phone_number = data.get('phone_number')
    password = data.get('password')

    if User.query.filter_by(phone_number=phone_number).first():
        return jsonify({'message': 'Phone number already exists'}), 400

    new_user = User(phone_number=phone_number)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

def login():
    data = request.get_json()
    phone_number = data.get('phone_number')
    password = data.get('password')

    user = User.query.filter_by(phone_number=phone_number).first()

    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@jwt_required()
def create_wallet():
    user_id = get_jwt_identity()
    binance_service = BinanceService()
    wallet_address = binance_service.create_wallet()

    new_wallet = Wallet(user_id=user_id, address=wallet_address)
    db.session.add(new_wallet)
    db.session.commit()

    return jsonify({'message': 'Wallet created successfully', 'wallet_address': wallet_address}), 201

@jwt_required()
def connect_wallet():
    user_id = get_jwt_identity()
    data = request.get_json()
    wallet_address = data.get('wallet_address')

    if Wallet.query.filter_by(address=wallet_address).first():
        return jsonify({'message': 'Wallet already exists'}), 400

    new_wallet = Wallet(user_id=user_id, address=wallet_address)
    db.session.add(new_wallet)
    db.session.commit()

    return jsonify({'message': 'Wallet connected successfully'}), 201

@jwt_required()
def view_wallets():
    user_id = get_jwt_identity()
    wallets = Wallet.query.filter_by(user_id=user_id).all()
    wallet_list = [{'id': wallet.id, 'address': wallet.address} for wallet in wallets]
    return jsonify(wallet_list), 200

@jwt_required()
def view_total_balance():
    user_id = get_jwt_identity()
    binance_service = BinanceService()
    total_balance = binance_service.get_total_balance(user_id)
    return jsonify(total_balance), 200

@jwt_required()
def view_wallet_balance(wallet_id):
    binance_service = BinanceService()
    balance = binance_service.get_wallet_balance(wallet_id)
    return jsonify(balance), 200

@jwt_required()
def send_assets():
    data = request.get_json()
    from_wallet = data.get('from_wallet')
    to_wallet = data.get('to_wallet')
    amount = data.get('amount')

    binance_service = BinanceService()
    transaction = binance_service.send_assets(from_wallet, to_wallet, amount)

    return jsonify(transaction), 200

@jwt_required()
def view_transactions_history():
    user_id = get_jwt_identity()
    binance_service = BinanceService()
    transactions = binance_service.get_transactions_history(user_id)
    return jsonify(transactions), 200
