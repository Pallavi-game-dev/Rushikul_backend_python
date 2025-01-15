

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.schema import branchData
from src.database import getDB
from src import models


router = APIRouter(tags=["Branch"])

@router.get("/get_branch",tags=["Branch"])
def getBarnch(
        db:Session= Depends(getDB)
):
    try:
        branch = db.query(
            models.Branch.branch_id,
            models.Branch.branch_name,
            models.Branch.branch_location
            ).all()
        branch_list = [
            {
                "branch_id":item.branch_id,
                "branch_name":item.branch_name,
                "branch_location":item.branch_location,
            } for item in branch
        ]
        return branch_list        
    except Exception as e :
        print(e)
    
@router.get("/add_branch",tags=["Branch"])
def createNewBranch(
    branch = branchData,
    db:Session = Depends(getDB)
):
    try:
        branch = dict(branch)
        new_data = models.Branch(
            branch_name=branch['branch_name'],
            branch_location=branch['branch_location'],
        )
        db.add(new_data)
        db.commit()
        db.refresh(new_data)
        return new_data
    except Exception as e :
        print(e)

