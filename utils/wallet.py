import requests
from config import Config

def create_new_wallet():
    response = requests.post(f"{Config.BLOCKCHAIN_API_URL}/wallets/new")
    return response.json()

def connect_existing_wallet(wallet_address, private_key):
    payload = {
        "wallet_address": wallet_address,
        "private_key": private_key
    }
    response = requests.post(f"{Config.BLOCKCHAIN_API_URL}/wallets/connect", json=payload)
    return response.json()