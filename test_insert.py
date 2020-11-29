from models import Session, User

session = Session()

user = User(first_name="me", last_name="mine", password="password", user_name="user_name")

session.add(user)
session.commit()