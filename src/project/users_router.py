from typing import Union
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.schema import CustomerBase, RoleEnum, UpadteUserData, UserData
from src import models
from sqlalchemy import or_
from src.database import getDB
from src.utils import getResponse
router = APIRouter(tags=["User"])




@router.get("/get_user_details",tags=['User'])
def getUserDetails(
    db:Session= Depends(getDB)
):
    try:
        user = db.query(
            models.User.user_id,
            models.User.role_id,
            models.User.branch_id,
            models.User.user_name,
            models.User.user_email,
            models.User.mobile_number,
            models.User.manager_id,
        ).all()

        user_data=[
            {
                "user_id":item.user_id,
                "role_id":item.role_id,
                "branch_id":item.branch_id,
                "user_name":item.user_name,
                "user_email":item.user_email,
                "mobile_number":item.mobile_number,
                "manager_id":item.manager_id,
            } for item in user
        ]
        return getResponse(True,user_data,"Users get succesfully")
    except Exception as e :
         return getResponse(False, {"data": repr(e)})


@router.post('/add_user',tags=['User'])
def createUser(
    user_data:UserData,
    db:Session= Depends(getDB)
):
    try:

        user_data = user_data.dict()
        check_user_exist = db.query(models.User).filter(
            or_(
                models.User.user_email == user_data["user_email"],
                models.User.mobile_number == user_data["mobile_number"]
            )).first()
        if check_user_exist is not None:
            return  getResponse(False,"User Already Exist")  
        else:
            new_data=models.User(
                role_id=user_data['role_id'],
                branch_id=user_data['branch_id'],
                user_name=user_data['user_name'],
                user_email=user_data['user_email'],
                manager_id=user_data['manager_id'],
                mobile_number=user_data['mobile_number']
            )
            db.add(new_data)
            db.commit()
            db.refresh(new_data)
            return getResponse(True,new_data,"User added succesfully")

    except Exception as e:
        return getResponse(False, {"data": repr(e)})



@router.get("/get_user_director",tags=['User'])
def getUserDetails(
    db:Session= Depends(getDB)
):
    try:
        director_role = list(db.query(models.Role.role_id).filter(models.Role.role_name==RoleEnum.director).first())
        # print("director_role",director_role)
        user = db.query(
            models.User.role_id,
            models.User.branch_id,
            models.User.user_name,
            models.User.user_email,
            models.User.mobile_number,
            models.User.manager_id,
                       
        ).filter(models.User.role_id==director_role[0]).all()

        user_data=[
            {
                "role_id":item.role_id,
                "branch_id":item.branch_id,
                "user_name":item.user_name,
                "user_email":item.user_email,
                "mobile_number":item.mobile_number,
            } for item in user
        ]
        

        return getResponse(True,user_data,'Director get succesfully')
    except Exception as e :
        return getResponse(False, {"data": repr(e)})

@router.get("/get_user_agent",tags=['User'])
def getUserDetails(
    db:Session= Depends(getDB)
):
    try:
        agent_role = list(db.query(models.Role.role_id).filter(models.Role.role_name==RoleEnum.agent).first())
        # print("agent_role",agent_role)
        user = db.query(
            models.User.role_id,
            models.User.branch_id,
            models.User.user_name,
            models.User.user_email,
            models.User.mobile_number,
            models.User.manager_id,                       
        ).filter(models.User.role_id==agent_role[0]).all()

        user_data=[
            {
                "role_id":item.role_id,
                "branch_id":item.branch_id,
                "user_name":item.user_name,
                "user_email":item.user_email,
                "mobile_number":item.mobile_number,
            } for item in user
        ]
        return getResponse(True,user_data,'Agent get succesfully')
    except Exception as e :
        return getResponse(False, {"data": repr(e)})

@router.post('/update_user',tags=['User'])
def updateUser(
    user_data:UpadteUserData,
    db:Session= Depends(getDB)
):
    try:
        user_data_dict = user_data.dict()
        existing_user  = db.query(models.User).filter(models.User.user_id == user_data_dict["user_id"]).first()
        if not existing_user:
            return getResponse(False,"User Not Found")

        check_duplicateEntry = db.query(models.User).filter(
            models.User.user_id != user_data_dict["user_id"],
            or_(
                models.User.user_email == user_data_dict["user_email"],
                models.User.mobile_number == user_data_dict["mobile_number"]
            )
        ).first()
        if check_duplicateEntry is not None:
            return getResponse(False,"User with Same Email/Mobile is Already register ")
        
       
       
        db.query(models.User).filter(models.User.user_id == user_data_dict["user_id"]).update(
            {
                "user_name": user_data_dict["user_name"],
                "role_id": user_data_dict["role_id"],
                "branch_id": user_data_dict["branch_id"],
                "user_email": user_data_dict["user_email"],
                "mobile_number": user_data_dict["mobile_number"],
                "manager_id": user_data_dict["manager_id"],
            }
        )
        db.commit()
        return getResponse(True, user_data_dict, "User Details Updated Successfully")

    except Exception as e:
        return getResponse(False, {"data": repr(e)})
