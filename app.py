from flask import Flask, request
import user_service
import wallet_service
import transaction_service
from flask_httpauth import HTTPBasicAuth
from models import User

app = Flask("__name__")

auth = HTTPBasicAuth()

@app.route("/api/v1/hello-world-1")
def index():
    return "Hello World-1"


@app.route("/api/v1/users", methods=["POST"])
def create_user():
    userDTO = request.get_json()
    response = user_service.create_user(userDTO)
    return response.get_json(), response.code


@app.route("/api/v1/users", methods=["GET"])
@auth.login_required
def get_user_by_id():
    this_user = auth.current_user()
    response = user_service.get_user_by_id(this_user.id)
    return response.get_json(), response.code


@app.route("/api/v1/users/<int:user_id>", methods=["PUT"])
@auth.login_required
def update_user(user_id):
    this_user = auth.current_user()
    userDTO = request.get_json()
    if user_id != this_user.id:
        return "Not authorized", 401
    response = user_service.update_user(user_id, userDTO)
    return response.get_json(), response.code


@app.route("/api/v1/wallets", methods=["POST"])
@auth.login_required
def create_wallet():
    this_user = auth.current_user()
    walletDTO = request.get_json()
    if walletDTO['user_id'] != this_user.id:
        return "Not authorized", 401
    response = wallet_service.create_wallet(walletDTO)
    return response.get_json(), response.code


@app.route("/api/v1/wallets", methods=["GET"])
@auth.login_required
def get_user_wallets():
    this_user = auth.current_user()
    response = wallet_service.get_user_wallets(this_user.id)
    return response.get_json(), response.code


@app.route("/api/v1/wallets/<int:wallet_id>", methods=["PUT"])
@auth.login_required
def update_wallet(wallet_id):
    wallet_dto = request.get_json()
    response = wallet_service.update_wallet(wallet_id, wallet_dto)
    return response.get_json(), response.code

@app.route("/api/v1/transactions", methods=["POST"])
@auth.login_required
def process_transaction():
    this_user = auth.current_user()
    transaction_dto = request.get_json()

    if transaction_dto['sender_id'] != this_user.id:
        return "Not authorized", 401

    response = transaction_service.create_transaction(transaction_dto)
    return response.get_json(), response.code

@auth.verify_password
def process_auth(user_name, password):
  return user_service.auth(user_name, password)

if __name__ == '__main__':
    app.run()