from fastapi import FastAPI
from .routes import market_place, purchase, users,auth
import uvicorn,os
from dotenv import load_dotenv
app = FastAPI()
load_dotenv()
PORT=int(os.getenv('PORT', '8000'))

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(market_place.router)
app.include_router(purchase.router)

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0',port=PORT)  


