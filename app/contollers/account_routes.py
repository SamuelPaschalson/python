from flask import Blueprint
from app.controllers import account_controller

account_bp = Blueprint('accounts', __name__)

account_bp.route('/signup', methods=['POST'])(account_controller.signup)
account_bp.route('/login', methods=['POST'])(account_controller.login)
account_bp.route('/create-wallet', methods=['POST'])(account_controller.create_wallet)
account_bp.route('/connect-wallet', methods=['POST'])(account_controller.connect_wallet)
account_bp.route('/wallets', methods=['GET'])(account_controller.view_wallets)
account_bp.route('/total-balance', methods=['GET'])(account_controller.view_total_balance)
account_bp.route('/wallet-balance/<int:wallet_id>', methods=['GET'])(account_controller.view_wallet_balance)
account_bp.route('/send-assets', methods=['POST'])(account_controller.send_assets)
account_bp.route('/transactions-history', methods=['GET'])(account_controller.view_transactions_history)
