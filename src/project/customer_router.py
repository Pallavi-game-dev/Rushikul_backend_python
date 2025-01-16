from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy import or_
from sqlalchemy.orm import Session
from src.schema import CustomerBase, getUser
from src import models
from src.database import getDB
from src.utils import getResponse
router = APIRouter(tags=["Customer"])



@router.post("/get_customer_details",tags=['Customer'])
def getCustomerDetails(
    customer_filter:getUser,
    db:Session= Depends(getDB)
):
    try:

        customer_filter = customer_filter.dict()
        print("customer_filter",customer_filter)
        customers_query = db.query(
            models.Customer.customer_first_name,
            models.Customer.customer_last_name,
            models.Customer.customer_email,
            models.Customer.mobile_number,
            models.Customer.gender,
            models.Customer.address,
            models.Customer.enabled,
            models.Customer_adharcard_kyc.addharcard_number,
            models.CustomerPancardKyc.pancard_number            
        ).join(
            models.Customer_adharcard_kyc,
            models.Customer_adharcard_kyc.customer_id==models.Customer.customer_id
        ).join(
            models.CustomerPancardKyc,
            models.CustomerPancardKyc.customer_id==models.Customer.customer_id
        )

          # Filter by customer type
        if customer_filter["customer_type"]:
            if 'active' in customer_filter["customer_type"]:
                customers_query = customers_query.filter(models.Customer.enabled.is_(True))
            if 'inactive' in customer_filter["customer_type"]:
                customers_query = customers_query.filter(models.Customer.enabled.is_(False))

        # Filter by finder_string
        if customer_filter["finder_string"]:
            value = customer_filter["finder_string"]
            customers_query = customers_query.filter(
                or_(
                    models.Customer.customer_first_name.ilike(f"%{value}%"),
                    models.Customer.customer_last_name.ilike(f"%{value}%"),
                    models.Customer.customer_email.ilike(f"%{value}%"),
                    models.Customer.mobile_number.ilike(f"%{value}%"),
                    models.Customer.address.ilike(f"%{value}%"),
                    models.Customer_adharcard_kyc.addharcard_number.ilike(f"%{value}%"),
                    models.CustomerPancardKyc.pancard_number.ilike(f"%{value}%")
                )
            )

        customers_query.all()
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
        } for item in customers_query
        ]
        return getResponse(True, customer_data,'Data get succesfully')
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
            
