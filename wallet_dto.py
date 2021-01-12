from models import Wallet
from marshmallow import Schema, fields


class WalletDto(Schema):
    class Meta:
        model = Wallet
        fields = ("id", "balance", "is_default", "owner_id")
