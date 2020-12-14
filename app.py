from flask import Flask, request
import user_service
import wallet_service

app = Flask("__name__")


@app.route("/api/v1/hello-world-1")
def index():
    return "Hello World-1"


@app.route("/api/v1/users", methods=["POST"])
def create_user():
    userDTO = request.get_json()
    response = user_service.create_user(userDTO)
    return response.get_json(), response.code


@app.route("/api/v1/users/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id):
    response = user_service.get_user_by_id(user_id)
    return response.get_json(), response.code


@app.route("/api/v1/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    userDTO = request.get_json()
    response = user_service.update_user(user_id, userDTO)
    return response.get_json(), response.code


@app.route("/api/v1/wallets", methods=["POST"])
def create_wallet():
    walletDTO = request.get_json()
    response = wallet_service.create_wallet(walletDTO)
    return response.get_json(), response.code


@app.route("/api/v1/wallets", methods=["GET"])
def get_user_wallets():
    user_id = request.args.get('user_id')
    response = wallet_service.get_user_wallets(user_id)
    return response.get_json(), response.code


if __name__ == '__main__':
    app.run()
