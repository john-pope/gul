from typing import List

from database import database
from database.tables import arpentries
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from gul.models import ARPEntry, LookupResults
from gul.repositories.query import gul_lookup
from gul.types import InvalidRequestException

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.exception_handler(InvalidRequestException)
async def invalid_request_handler(request: Request, error: InvalidRequestException):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"message": f"{error}", "value": error.value},
    )


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
def read_root():
    return {}


@app.get("/lookup/{search}", response_model=LookupResults)
async def lookup(search: str):
    return await gul_lookup(search)
