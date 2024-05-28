from flask import Blueprint, request, jsonify
from models import User, get_user, create_user, Session

crud = Blueprint("crud", __name__)

@crud.route("/users", methods=["GET"])
def get_users():
    session = Session()
    users = session.query(User).all()
    session.close()
    return jsonify([user.__dict__ for user in users])

@crud.route("/users", methods=["POST"])
def create_user_api():
    data = request.get_json()
    email = data["email"]
    username = data["username"]
    password = data["password"]
    sector = data.get("setor", "")
    create_user(email, username, password, sector)
    return {"message": "User created successfully"}

@crud.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    session = Session()
    user = session.query(User).get(user_id)
    if user:
        user.username = data["username"]
        user.sector = data["setor"]
        session.commit()
        session.close()
        return {"message": "Usuário atualizado com sucesso!"}
    else:
        session.close()
        return {"message": "User not found"}, 404
