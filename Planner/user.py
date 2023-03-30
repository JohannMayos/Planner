from datetime import datetime
from flask import abort, make_response
from database import engine
import json
from sqlalchemy import text

def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

USER = {
    "1000": {
        "user_name": "Caio Rolando da Rocha",
        "user_id": "1000",
        "timestamp": get_timestamp(),
    },
    "2000": {
        "user_name": "Jucimar Maia da Silva Jr",
        "user_id": "2000",
        "timestamp": get_timestamp(),
    },
    "3000": {
        "user_name": "Cthonem Martins",
        "user_id": "3000",
        "timestamp": get_timestamp(),
    }
}


def load_users_from_db():

    with engine.connect() as conn:
        result = conn.execute(text("select * from agenda_usuario"))
        column_names = result.keys()
        users = []
        for row in result.all():
            users.append(dict(zip(column_names, row)))
        return users


def create_users_from_db(user_id, user_name, user_email, user_password, user_status):

    with engine.connect() as conn:
        query = text("insert into agenda_usuario values('{id}','{name}','{email}','{password}','{status}')".format(id = user_id, name = user_name, email = user_email, password = user_password, status = user_status))
        conn.execute(query)


def get_user_by_id(user_id):
    with engine.connect() as conn:
        query = text("select * from agenda_usuario where usuario_id = '{id}'".format(id=user_id))
        result = conn.execute(query)
        user_data = result.fetchone()
        if user_data:
            user = {
                'id': user_data[0],
                'name': user_data[1],
                'email': user_data[2],
                'password': user_data[3],
                'status': user_data[4]
            }
            return user
        else:
            return None


def delete_user_by_id(user_id):
    with engine.connect() as conn:
        query = text("DELETE FROM agenda_usuario WHERE usuario_id = '{id}'".format(id=user_id))
        result = conn.execute(query)
        if result.rowcount == 0:
            return None
        else:
            return {"Usuário Deletado": user_id}


def update_user_by_id(user_id, name, email, password, status):
    with engine.connect() as conn:
        # Verifica se todos os campos estão preenchidos
        if not name and not email and not password and not status:
            return None
        
        # Atualiza os campos não nulos
        query = text("UPDATE agenda_usuario SET "
                     "usuario_nome = COALESCE(:name, usuario_nome), "
                     "usuario_email = COALESCE(:email, usuario_email), "
                     "usuario_senha = COALESCE(:password, usuario_senha), "
                     "usuario_status = COALESCE(:status, usuario_status) "
                     "WHERE usuario_id = :user_id")
        conn.execute(query, {'name': name or None, 'email': email or None, 'password': password or None, 'status': status or None, 'user_id': user_id})


def read_all():
    return list(load_users_from_db())


def create(user):
    user_id = user.get("user_id")
    user_name = user.get("user_name", "")
    user_email = user.get("user_email", "")
    user_password = user.get("user_password", "")
    user_status = user.get("user_status", "")

    if user_id and user_id not in USER:
       create_users_from_db(user_id, user_name, user_email, user_password, user_status)
    else:
        abort(
            406,
            f"User with last name {user_id} already exists",
        )


def read_one(user_id):
    user = get_user_by_id(user_id)
    if user is not None:
        return user
    else:
        abort(
            404, f"Person with ID {user_id} not found"
        )


def update(user_id, name, email, password, status):
    with engine.connect() as conn:
        # Verifica se o usuário existe antes de atualizar
        result = conn.execute(text("SELECT COUNT(*) FROM agenda_usuario WHERE usuario_id = :user_id"), {'user_id': user_id}).fetchone()
        if result[0] == 0:
            abort(404, f"Person with ID {user_id} not found")

        # Chama a função para atualizar o usuário
        user = update_user_by_id(user_id, name, email, password, status)
        if user is not None:
            return user
        else:
            abort(404, f"Person with ID {user_id} not found")



def delete(user_id):
    user = delete_user_by_id(user_id)
    if user is not None:
        return user
    else:
        abort(
            404, f"Person with ID {user_id} not found"
        )
