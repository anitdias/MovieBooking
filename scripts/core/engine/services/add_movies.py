import os

import jwt
from fastapi import APIRouter, HTTPException

from scripts.logging.logger import logger
from scripts.utils.mongo_utils import db
from scripts.schema.movie_schemas import MovieDetails

movie_collection = db["movie_collection"]
add_movie_router = APIRouter()

jwt_key = os.getenv('SECRET_KEY')
algorithm = os.getenv('ALGORITHM')


@add_movie_router.post('/addMovie')
def add_movie(movie: MovieDetails, token: str):
    try:
        decoded_token = jwt.decode(token, jwt_key, algorithms=[algorithm])
        username = decoded_token.get('user')
        if not username == "admin":
            raise HTTPException(status_code=401, detail="Only Admin access")
        else:
            movie_collection.insert_one(dict(movie))
            logger.info("Movie added to database")
    except Exception as e:
        logger.exception(f"error in {e}")
        print(e)
        return {"error": "Error while adding movie"}
