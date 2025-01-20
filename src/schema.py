from enum import Enum
from pydantic import BaseModel, Field, constr
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
    email: str = constr(strip_whitespace=True,pattern=r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")
    mobile_number: int = constr(strip_whitespace=True,pattern=r"[0-9]+", min_length=10, max_length=10)
    gender: GenderEnum
    aadharcard: str
    pancard: str
    branch_id: int
    address: str

class UpdateCustomerBase(BaseModel):
    customer_id:int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = constr(strip_whitespace=True,pattern=r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")
    mobile_number: Optional[int] = constr(strip_whitespace=True,pattern=r"[0-9]+", min_length=10, max_length=10)
    gender: Optional[GenderEnum] = None
    aadharcard: Optional[str] = None
    pancard: Optional[str] = Field(None,pattern=r"^[a-zA-Z]{3}[p|P|c|C|h|H|f|F|a|A|t|T|b|B|l|L|j|J|g|G][A-Za-z][\d]{4}[A-Za-z]$",)
    branch_id: Optional[int] = None
    address: Optional[str] = None



class getUser(BaseModel):
    finder_string: str = None
    customer_type: Optional[List[str]] = None


class UserData(BaseModel):
    user_name:str
    role_id:int
    branch_id:int
    user_email:str = constr(strip_whitespace=True,pattern=r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")
    mobile_number:int=constr(strip_whitespace=True,pattern=r"[0-9]+", min_length=10, max_length=10)
    manager_id:int

class UpadteUserData(BaseModel):
    user_id:int
    user_name:str=None
    role_id:int=None
    branch_id:int=None
    user_email:str=constr(strip_whitespace=True,pattern=r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")
    mobile_number:int=constr(strip_whitespace=True,pattern=r"[0-9]+", min_length=10, max_length=10)
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