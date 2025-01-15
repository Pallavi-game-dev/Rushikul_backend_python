from enum import Enum
from pydantic import BaseModel
from typing import Union


class GenderEnum(str,Enum):
    male = "MALE"
    female = "FEMALE"

class  RoleEnum(str,Enum):
    owner = "Owner"
    general_manager = "General Manager"
    branch_manager = "Branch Manager"
    employee="Employee"
    agent="Agent"
    director="Director"

class CustomerBase(BaseModel):
    first_name: str
    last_name: str
    email: str=None
    phone: str
    gender: GenderEnum
    aadharcard: int
    pancard: str
    branch_id: int
    address: str

class UserData(BaseModel):
    user_name:str
    role_id:int
    branch_id:int
    user_email:str
    mobile_number:int
    manager_id:int

class branchData(BaseModel):
    branch_name:str
    branch_location:str

class CreateLoan(BaseModel):
    customer_id:int
    loan_amount:str
    intrest_rate:str
    loan_start_date:str
    loan_end_date:str
    created_by:str