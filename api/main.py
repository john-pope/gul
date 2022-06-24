from typing import List

from fastapi import FastAPI

from gul.models import ARPEntry

from database import database
from database.tables import arpentries
from gul.query import gul_lookup


app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/")
def read_root():
    return {}

@app.get("/test-imperative", response_model=List[ARPEntry])
async def test():
    q = arpentries.select().limit(10)
    return await database.fetch_all(q)

@app.get("/test-raw")
async def test():
    q = "select * from arpentries limit 10"
    return await database.fetch_all(q)


@app.get("/lookup/{search}")
async def lookup(search: str):
    return await gul_lookup(search)
