from app.extensions import db

class Wallet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    address = db.Column(db.String(64), unique=True, nullable=False)
    user = db.relationship('User', back_populates='wallets')

User.wallets = db.relationship('Wallet', order_by=Wallet.id, back_populates='user')