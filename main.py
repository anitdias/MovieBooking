from fastapi import FastAPI

from scripts.core.engine.services.add_movies import add_movie_router
from scripts.core.engine.services.book_seats import seat_booking_router
from scripts.core.engine.services.list_movies import list_movie_router
from scripts.core.engine.services.user_authentication import user_auth_route

app = FastAPI()

app.include_router(user_auth_route)
app.include_router(add_movie_router)
app.include_router(list_movie_router)
app.include_router(seat_booking_router)
