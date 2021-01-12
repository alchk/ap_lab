from models import User, Wallet, Session
from http_response import HttpResponse
from wallet_dto import WalletDto

session = Session()
wallets_dto = WalletDto(many=True)


def create_wallet(wallet_dto):
    try:
        user = session.query(User).filter_by(id=int(wallet_dto['user_id'])).one()
    except:
        return HttpResponse("NOT_FOUND", 404)

    wallets = session.query(Wallet).filter_by(owner_id=int(wallet_dto['user_id'])).all()

    if len(wallets) >= 1:
        wallet = Wallet(balance=0, owner_id=wallet_dto['user_id'], is_default=False)
    else:
        wallet = Wallet(balance=0, owner_id=wallet_dto['user_id'], is_default=True)

    session.add(wallet)
    session.commit()
    return HttpResponse("SUCCESSFULLY_CREATED_WALLET", 201)


def get_user_wallets(user_id):
    try:
        wallets = session.query(Wallet).filter_by(owner_id=int(user_id)).all()
    except:
        return HttpResponse("NO_WALLETS", 404)
    return HttpResponse(wallets_dto.dump(wallets), 200)


def update_wallet(wallet_id, wallet_dto):
    try:
        wallet = session.query(Wallet).filter_by(id=int(wallet_id)).one()
    except:
        return HttpResponse("WALLET_NOT_FOUND", 404)

    try:
        if wallet_dto.get('balance', -100):
            update_amount = int(wallet_dto['balance'])
            if update_amount <= 0:
                return HttpResponse("BAD_AMOUNT", 405)
            else:
                wallet.balance += int(wallet_dto['balance'])
        if wallet_dto.get('is_default', None):
            wallet.is_default = wallet_dto['is_default']
    except:
        return HttpResponse("INVALID_INPUT", 405)

    session.commit()
    return HttpResponse("WALLET_UPDATED", 200)
