import os

import jwt
from fastapi import APIRouter

from scripts.constants.app_constanst import Constants
from scripts.logging.logger import logger
from scripts.utils.mongo_utils import db
from scripts.schema.movie_schemas import BookSeat

jwt_key = os.getenv('SECRET_KEY')
algorithm = os.getenv('ALGORITHM')
movie_collection = db[Constants.movie_collection]
user_booking_collection = db[Constants.user_booking_collection]

seat_booking_router = APIRouter()


@seat_booking_router.post('/book')
def book_seats(seat: BookSeat, token: str):
    decoded_token = jwt.decode(token, jwt_key, algorithms=[algorithm])
    username = decoded_token.get('user')
    booking_failed = False
    booking_request = []
    if movie_collection.find_one({"name": seat.name}):
        movie_details = movie_collection.find_one({"name": seat.name})
        lst = list(seat.seat_no)
        seat_lst = movie_details['seats']
        for i in lst:
            booking_failed = False
            if i in seat_lst:
                booking_failed = True
                booking_request.append(i)

        if booking_failed:
            print(f"seat not available {booking_request}")
            logger.info(f"seat not available {booking_request}")
        else:
            for i in lst:
                seat_lst.append(i)

        movie_collection.update_one({"name": seat.name}, {"$set": {'seats': seat_lst}})
        user_booking_collection.insert_one(
            {'username': username, 'movie_name': movie_details['name'], 'seat': lst})
        logger.info("Booked seats")
