from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.schema import CustomerBase
from src import models
from src.database import getDB
router = APIRouter(tags=["Customer"])



@router.get("/get_customer_details",tags=['Customer'])
def getCustomerDetails(
    db:Session= Depends(getDB)
):
    try:
        customers = db.query(
            models.Customer.customer_first_name,
            models.Customer.customer_last_name,
            models.Customer.customer_email,
            models.Customer.mobile_number,
            models.Customer.gender,
            models.Customer.address,
            models.Customer_adharcard_kyc.addharcard_number,
            models.CustomerPancardKyc.pancard_number            
        ).join(
            models.Customer_adharcard_kyc,
            models.Customer_adharcard_kyc.customer_id==models.Customer.customer_id
        ).join(
            models.CustomerPancardKyc,
            models.CustomerPancardKyc.customer_id==models.Customer.customer_id
        ).all()

        customer_data=[
            {
                "customer_first_name":item.customer_first_name,
                "customer_last_name":item.customer_last_name,
                "customer_email":item.customer_email,
                "mobile_number":item.mobile_number,
                "gender":item.gender,
                "address":item.address,
                "addharcard_number":item.addharcard_number,
                "pancard_number":item.pancard_number
            } for item in customers
        ]
        

        return customer_data
    except Exception as e :
        print(e)


@router.post("/add_customer",tags=['Customer'])
def addcustomer(
    customer_data:CustomerBase,
    db:Session= Depends(getDB)
):
    try:
       customer_data=dict(customer_data)
       print(customer_data['first_name'])
       new_data=models.Customer(
          customer_first_name=customer_data['first_name'],
          customer_last_name=customer_data['last_name'],
          customer_email=customer_data['email'],
          mobile_number=customer_data['phone'],
          gender=customer_data['gender'],
          address=customer_data['address'],
          branch_id=customer_data['branch_id'],
       )
       db.add(new_data)
       db.commit()
       db.refresh(new_data)
    #    print(new_data.__dict__,"NEW")

       aadhar=models.Customer_adharcard_kyc(
           customer_id=new_data.customer_id,
           addharcard_number=customer_data['aadharcard']
       )
       db.add(aadhar)
       db.commit()
       db.refresh(aadhar)

       pancard = models.CustomerPancardKyc(
           customer_id = new_data.customer_id,
           pancard_number = customer_data['pancard']
       )
       db.add(pancard)
       db.commit()

       db.refresh(pancard)

       return customer_data
    except Exception as e :
        import traceback
        traceback.print_exc()
        print(e)
            
