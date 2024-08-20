from fastapi import APIRouter
from pydantic import BaseModel

from scripts.constants.app_constanst import Constants
from scripts.logging.logger import logger

movie_collection = Constants.movie_collection


class MovieName(BaseModel):
    name: str


list_movie_router = APIRouter()


@list_movie_router.get("/list")
def list_movies():
    try:
        movies = movie_collection.find()
        print(f"{"*" * 30}")
        print("MovieName\tDate\t\t\tTime")
        for movie in movies:
            print(movie["name"], "\t", movie["date"], "\t", movie['time'])
        print(f"{"*" * 30}")
        logger.info("Movies Listed")
    except Exception as e:
        logger.exception(f"error in {e}")
        print(e)
        return {"error": "Error while listing movie"}


@list_movie_router.post("/listSeats")
def list_available_seats(movie_name: MovieName):
    if movie_collection.find_one({"name": movie_name.name}):
        movie_details = movie_collection.find_one({"name": movie_name.name})
        print("## seats are occupied \n numbered seats are available")
        lst = movie_details['seats']
        num = 1
        for i in range(10):
            for j in range(10):
                if num <= 100 and num not in lst:
                    print(num, end="\t")
                    num += 1
                else:
                    print("##", end="\t")
                    num += 1
            print("\n")
        logger.info("available seats listed")
