from enum import Enum
from pydantic import BaseModel
from typing import List, Optional, Union


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

class UpdateCustomerBase(BaseModel):
    customer_id:int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    gender: Optional[GenderEnum] = None
    aadharcard: Optional[str] = None
    pancard: Optional[str] = None
    branch_id: Optional[int] = None
    address: Optional[str] = None



class getUser(BaseModel):
    finder_string: Optional[str] = None,
    customer_type: Optional[List[str]] = None,


class UserData(BaseModel):
    user_name:str
    role_id:int
    branch_id:int
    user_email:str
    mobile_number:int
    manager_id:int

class UpadteUserData(BaseModel):
    user_id:int
    user_name:str=None
    role_id:int=None
    branch_id:int=None
    user_email:str=None
    mobile_number:int=None
    manager_id:int=None

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