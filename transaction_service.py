from models import Transaction, Wallet, Session
from transaction_dto import TransactionDto
from http_response import HttpResponse
from datetime import datetime


session = Session()
transactions = TransactionDto(many=True)


def create_transaction(transaction_dto):
    if transaction_dto.get('amount') is not None:
        amount = int(transaction_dto['amount'])
        if amount <= 0:
            return HttpResponse("INVALID_AMOUNT", 405)
    else:
        return HttpResponse("AMOUNT_NOT_PRESENT", 405)

    sender_wallet = get_default_wallet('sender_id', transaction_dto)
    receiver_wallet = get_default_wallet('receiver_id', transaction_dto)
    if not isinstance(sender_wallet, Wallet) or not isinstance(receiver_wallet, Wallet):
        return receiver_wallet

    if sender_wallet.balance < amount:
        return HttpResponse("INSUFFICIENT_FUNDS", 405)

    transaction = Transaction(sender_id=int(transaction_dto['sender_id']), receiver_id=int(transaction_dto['receiver_id']), amount=amount, time_stamp=datetime.today())
    sender_wallet.balance = sender_wallet.balance - amount
    receiver_wallet.balance += amount

    session.add(transaction)
    session.commit()

    return HttpResponse(TransactionDto().dump(transaction), 201)


def get_default_wallet(attribute, transaction_dto):
    try:
        print(int(transaction_dto[attribute]))
        wallet = session.query(Wallet) \
            .filter_by(owner_id=int(transaction_dto[attribute])) \
            .filter_by(is_default=True) \
            .one()
        return wallet
    except:
        formatted = attribute.split('_')
        message = f'{formatted[0]} wallet was not found'
        return HttpResponse(message, 404)
