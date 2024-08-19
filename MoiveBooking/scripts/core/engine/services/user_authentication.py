import os
import bcrypt
import jwt
from fastapi import APIRouter, HTTPException
from scripts.utils.mongoutils import db
from pydantic import BaseModel
from scripts.constants.app_constanst import Constants
from scripts.logging.logger import logger

user_collection = db[Constants.user_collection]

user_auth_route = APIRouter()

jwt_key = os.getenv('SECRET_KEY')
algorithm = os.getenv('ALGORITHM')


class User(BaseModel):
    username: str
    password: str


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verify_password(stored_password: str, provided_password: str) -> bool:
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))


@user_auth_route.post("/signup")
def sign_up(user: User):
    try:
        if not user_collection.find_one({"username": user.username}):
            user.password = hash_password(user.password)
            user_collection.insert_one(dict(user))
            logger.info("User Created")
        else:
            logger.exception("Username already registered")
            raise HTTPException(status_code=400, detail="Username already registered")

    except Exception as e:
        print(e)
        logger.exception("Error in User SignUp")
        return {"msg": "Error in User SignUp"}


@user_auth_route.post('/login')
def login(user: User):
    try:
        if user_collection.find_one({"username": user.username}):
            user_credential = user_collection.find_one({"username": user.username})
            password_in_db = user_credential["password"]

            if verify_password(password_in_db, user.password):
                logger.info("User logged in, token returned")
                return jwt.encode({"user": user.username}, jwt_key, algorithm=algorithm)
            else:
                logger.exception("Incorrect Password")
                raise HTTPException(status_code=401, detail="Incorrect Password")
        else:
            logger.exception("Username does not exist")
            raise HTTPException(status_code=400, detail="Username does not exist")
    except Exception as e:
        print(e)
        logger.exception("Error in User Login")
        return {"msg": "Error in User Login"}
