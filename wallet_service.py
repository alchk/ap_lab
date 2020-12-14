from models import User, Wallet, Session
from http_response import HttpResponse
from wallet_dto import WalletDto

session = Session()
wallets_dto = WalletDto(many=True)


def create_wallet(wallet_dto):
    if wallet_dto.get('user_id', None):
        wallet = Wallet(balance=0, owner_id=wallet_dto['user_id'], is_default=True)
    else:
        return HttpResponse('INVALID_INPUT', 405)

    try:
        user = session.query(User).filter_by(id=int(wallet_dto['user_id'])).one()
    except:
        return HttpResponse("NOT_FOUND", 404)

    session.add(wallet)
    session.commit()
    return HttpResponse("SUCCESSFULLY_CREATED_WALLET", 201)


def get_user_wallets(user_id):
    try:
        print(user_id)
        wallets = session.query(Wallet).filter_by(owner_id=int(user_id)).all()
        print(wallets)
    except:
        return HttpResponse("NO_WALLETS", 404)

    return HttpResponse(wallets_dto.dump(wallets),200)