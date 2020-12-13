from datetime import datetime

from models import Session, User, Wallet, Transaction

session = Session()

user = User(first_name="me", last_name="mine", password="password", user_name="user_name")
user1 = User(first_name="notMe", last_name="notMine", password="Notpassword", user_name="Notuser_name")

wallet = Wallet(balance=100, owner_id=1, is_default=True)
wallet1 = Wallet(balance=100, owner_id=2, is_default=True)

transaction = Transaction(sender_id=1, receiver_id=2, amount=50, time_stamp=datetime.today())

session.add(user)
session.add(user1)
session.add(wallet)
session.add(wallet1)
session.add(transaction)
session.commit()