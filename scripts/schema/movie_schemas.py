from typing import List

from pydantic import BaseModel


class MovieDetails(BaseModel):
    name: str
    date: str
    time: str
    seats: List[str] = []


class BookSeat(BaseModel):
    name: str
    seat_no: List[int]


class MovieName(BaseModel):
    name: str


class User(BaseModel):
    username: str
    password: str
