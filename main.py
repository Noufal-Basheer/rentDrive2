from fastapi import FastAPI
from .routes import market_place, purchase, users,auth,home

from fastapi.staticfiles import StaticFiles
app = FastAPI()


app.mount("/static", StaticFiles(directory="api/static"),name="static")
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(market_place.router)
app.include_router(purchase.router)
app.include_router(home.router)




