from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src import models
from src.database import getDB
from src.utils import getResponse

router = APIRouter([tags="Deposits"])


@router('/get_deposits',tags=['Deposits'])
def getDeposits(
    db:Session=Depends(getDB)
)