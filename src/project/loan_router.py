 

from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from src.schema import CreateLoan
from src import models
from src.database import getDB

router = APIRouter(tags=["Loan"])



@router.get('/get_list_of_loan',tags=['Loan'])
def getLoanList(
    db:Session = Depends(getDB)

):
    try:
        loan_list = db.query(
            models.loan_type.loan_type_id,
            models.Customer.customer_first_name,
            models.Customer.customer_last_name,
            models.loan.loan_amount,
            models.loan.intrest_rate,
            models.loan.loan_start_date,
            models.loan.loan_end_date,
            models.loan.created_by,
            models.loan.created_at,
            ).join(
            models.loan_type,models.loan_type.loan_type_id==models.loan.loan_type_id
            ).join(
            models.Customer,models.Customer.customer_id==models.loan.customer_id)
        
        data = [
            {
            "loan_type_id":item.loan_type_id,
            "customer_first_name":item.customer_first_name,
            "customer_last_name":item.customer_last_name,
            "loan_amount":item.loan_amount,
            "intrest_rate":item.intrest_rate,
            "loan_start_date":item.loan_start_date,
            "loan_end_date":item.loan_end_date,
            "created_by":item.created_by,
            "created_at":item.created_at,
         
            }for item in loan_list
        ] 
        print("loan_list",data)
        return data
       
    except Exception as e:
        print(e)

@router.post('add_new_loan',tags=['Loan'])
def createLoan(
    data = CreateLoan,
    db:Session = Depends(getDB)
):
    data = dict(data)
    try:
        new_data = models.loan(
            customer_id=data['customer_id'],
            loan_type_id=data['loan_type_id'],
            loan_amount=data['loan_amount'],
            intrest_rate=data['intrest_rate'],
            loan_start_date=data['loan_start_date'],
            loan_end_date=data['loan_end_date']
        )
        db.add(new_data)
        db.commit()
        db.refresh()
        

    except Exception as e:
        print(e)
