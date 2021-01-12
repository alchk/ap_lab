from models import User
from marshmallow import Schema, fields


class UserDto(Schema):
    class Meta:
        model = User
        fields = ("id", "user_name", "first_name", "last_name")