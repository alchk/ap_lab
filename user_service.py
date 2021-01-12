from models import User, Session
from user_dto import UserDto
from http_response import HttpResponse

session = Session()


def create_user(user_dto):
    try:
        user = User(**user_dto)
    except:
        return HttpResponse("INVALID_INPUT", 405)

    session.add(user)
    session.commit()
    return HttpResponse("USER_CREATED", 201)


def get_user_by_id(user_id):
    try:
        user = session.query(User).filter_by(id=int(user_id)).one()
    except:
        return HttpResponse("USER_NOT_FOUND", 404)

    return HttpResponse(UserDto().dump(user), 200)


def update_user(user_id, data):
    try:
        user = session.query(User).filter_by(id=int(user_id)).one()
    except:
        return HttpResponse("NOT_FOUND", 404)

    try:
        if data.get('first_name', None):
            user.first_name = data['first_name']
        if data.get('last_name', None):
            user.last_name = data['last_name']
        if data.get('user_name', None):
            user.user_name = data['user_name']
        if data.get('password', None):
            user.password = data['password']
    except:
        return HttpResponse("INVALID_INPUT", 405)
    session.commit()

    return HttpResponse("USER_UPDATED", 200)

def auth(username, password):

    try:
        user = session.query(User).filter_by(user_name=username).one()
    except:
        return None

    if user.password == password:
        return user

