import os
from typing import List

import jwt
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from scripts.constants.app_constanst import Constants
from scripts.logging.logger import logger

movie_collection = Constants.movie_collection
add_movie_router = APIRouter()

jwt_key = os.getenv('SECRET_KEY')
algorithm = os.getenv('ALGORITHM')


class MovieDetails(BaseModel):
    name: str
    date: str
    time: str
    seats: List[str] = []


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
