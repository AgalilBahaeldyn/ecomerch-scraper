from typing import Union

from fastapi import FastAPI
from routes.shopee import shopee
from routes.lazada import lazada

app = FastAPI()



app.include_router(shopee)
app.include_router(lazada)
