import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'mysecret')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///blockchain.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BLOCKCHAIN_API_URL = "https://api.blockchain.com/v3/exchange"
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwtsecret')
    OAUTH2_PROVIDER_TOKEN_EXPIRES_IN = 3600  # 1 hour
    PORT = os.getenv('PORT', 5000)  # Default port