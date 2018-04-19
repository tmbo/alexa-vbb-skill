from boto.dynamodb2.exceptions import ItemNotFound
from boto.dynamodb2.fields import HashKey
from boto.dynamodb2.table import Table

users = Table('sbahn_alex_users', schema=[HashKey('user_id')])


def get_user(user_id):
    return users.get_item(user_id=user_id)


def store_on_user(user_id, key, value):
    try:
        u = get_user(user_id)
        u[key] = value
        u.partial_save()
    except ItemNotFound:
        users.put_item({"user_id": user_id, key: value})
