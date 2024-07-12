import requests
from config import Config

def get_wallet_history(wallet_address):
    response = requests.get(f"{Config.BLOCKCHAIN_API_URL}/wallets/{wallet_address}/history")
    return response.json()

def get_wallet_balance(wallet_address):
    response = requests.get(f"{Config.BLOCKCHAIN_API_URL}/wallets/{wallet_address}/balance")
    return response.json()

def get_wallet_nft(wallet_address):
    response = requests.get(f"{Config.BLOCKCHAIN_API_URL}/wallets/{wallet_address}/nfts")
    return response.json()

def get_wallet_tokens(wallet_address):
    response = requests.get(f"{Config.BLOCKCHAIN_API_URL}/wallets/{wallet_address}/tokens")
    return response.json()

def p2p_transaction(sender_address, recipient_address, amount):
    payload = {
        "sender": sender_address,
        "recipient": recipient_address,
        "amount": amount
    }
    response = requests.post(f"{Config.BLOCKCHAIN_API_URL}/transactions/p2p", json=payload)
    return response.json()