from models import Transaction
from marshmallow import Schema, fields


class TransactionDto(Schema):
    class Meta:
        model = Transaction
        fields = ("id", "sender_id", "receiver_id", "amount", "time_stamp")