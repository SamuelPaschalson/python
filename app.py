from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import Config
from models import db, User, Wallet
from utils.auth import signup, login
from utils.blockchain import (
    get_wallet_history,
    get_wallet_balance,
    get_wallet_nft,
    get_wallet_tokens,
    p2p_transaction
)
from utils.wallet import create_new_wallet, connect_existing_wallet

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt = JWTManager(app)
    limiter = Limiter(app, key_func=get_remote_address, default_limits=["200 per day", "50 per hour"])

    @app.before_first_request
    def create_tables():
        db.create_all()

    @app.route('/signup', methods=['POST'])
    def user_signup():
        return signup()

    @app.route('/login', methods=['POST'])
    def user_login():
        return login()

    @app.route('/wallet/history/<wallet_address>', methods=['GET'])
    @jwt_required()
    @limiter.limit("10 per minute")
    def wallet_history(wallet_address):
        history = get_wallet_history(wallet_address)
        return jsonify(history)

    @app.route('/wallet/balance/<wallet_address>', methods=['GET'])
    @jwt_required()
    @limiter.limit("10 per minute")
    def wallet_balance(wallet_address):
        balance = get_wallet_balance(wallet_address)
        return jsonify(balance)

    @app.route('/wallet/nfts/<wallet_address>', methods=['GET'])
    @jwt_required()
    @limiter.limit("10 per minute")
    def wallet_nft(wallet_address):
        nfts = get_wallet_nft(wallet_address)
        return jsonify(nfts)

    @app.route('/wallet/tokens/<wallet_address>', methods=['GET'])
    @jwt_required()
    @limiter.limit("10 per minute")
    def wallet_tokens(wallet_address):
        tokens = get_wallet_tokens(wallet_address)
        return jsonify(tokens)

    @app.route('/wallet/p2p', methods=['POST'])
    @jwt_required()
    @limiter.limit("5 per minute")
    def wallet_p2p():
        data = request.json
        sender_address = data['sender']
        recipient_address = data['recipient']
        amount = data['amount']
        transaction = p2p_transaction(sender_address, recipient_address, amount)
        return jsonify(transaction)

    @app.route('/wallet/new', methods=['POST'])
    @jwt_required()
    @limiter.limit("5 per minute")
    def new_wallet():
        wallet = create_new_wallet()
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        new_wallet = Wallet(address=wallet['address'], owner=user)
        db.session.add(new_wallet)
        db.session.commit()
        return jsonify(wallet)

    @app.route('/wallet/connect', methods=['POST'])
    @jwt_required()
    @limiter.limit("5 per minute")
    def connect_wallet():
        data = request.json
        wallet_address = data['wallet_address']
        private_key = data['private_key']
        wallet = connect_existing_wallet(wallet_address, private_key)
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        existing_wallet = Wallet(address=wallet['address'], owner=user)
        db.session.add(existing_wallet)
        db.session.commit()
        return jsonify(wallet)

    return app
    
if __name__ == '__main__':
    # app.run(debug=True)
    app = create_app()
    app.run(host='0.0.0.0', port=5000)