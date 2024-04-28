from fastapi import FastAPI
from .routes import market_place, users,auth

app = FastAPI()


app.include_router(users.router)
app.include_router(auth.router)
app.include_router(market_place.router)

