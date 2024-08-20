from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

from scripts.constants.app_constanst import Constants

from scripts.logging.logger import logger

movie_collection = Constants.movie_collection
seat_booking_router = APIRouter()


class BookSeat(BaseModel):
    name: str
    seat_no: List[int]


@seat_booking_router.post('/book')
def book_seats(seat: BookSeat):
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
        logger.info("Booked seats")
