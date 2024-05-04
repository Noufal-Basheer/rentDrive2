from fastapi import FastAPI
from .routes import market_place, purchase, users,auth

app = FastAPI()


app.include_router(users.router)
app.include_router(auth.router)
app.include_router(market_place.router)
app.include_router(purchase.router)



