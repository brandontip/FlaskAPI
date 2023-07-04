from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
import uuid
from db import db
from sqlalchemy.exc import SQLAlchemyError
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import create_access_token

from Models.user import UserModel
from schemas import UserSchema

blp = Blueprint("Users", "users", description="Operations on users.")

@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter_by(username=user_data["username"]).first()
        if user and sha256.verify(user_data["password"], user.password_hash):
            access_token = create_access_token(identity=user.id)
            return {"message": "Logged in", "access_token": access_token}
        else:
            abort(401, message="Invalid credentials.")

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        try:
            user = UserModel(username=user_data["username"], password_hash=sha256.hash(user_data["password"]))
        except Exception as e:
            abort(500, message="Failed to add user to database." + str(e))
        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message="Failed to add user to database." + str(e))
        return {"message": "User created successfully.", "user_id": user.id}

@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted."}


