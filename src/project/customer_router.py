from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy import or_
from sqlalchemy.orm import Session
from src.schema import CustomerBase, UpdateCustomerBase, getUser,DisabledCustomer
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
            models.Customer.customer_id,
            models.Customer.customer_first_name,
            models.Customer.customer_last_name,
            models.Customer.customer_email,
            models.Customer.mobile_number,
            models.Customer.gender,
            models.Customer.address,
            models.Customer.branch_id,
            models.Customer.enabled,
            models.Customer_adharcard_kyc.addharcard_number,
            models.CustomerPancardKyc.pancard_number            
        ).outerjoin(
            models.Customer_adharcard_kyc,
            models.Customer_adharcard_kyc.customer_id==models.Customer.customer_id
        ).outerjoin(
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
        print(customers_query)
        customer_data=[
        {
            "customer_id":item.customer_id,
            "customer_first_name":item.customer_first_name,
            "customer_last_name":item.customer_last_name,
            "customer_email":item.customer_email,
            "mobile_number":item.mobile_number,
            "gender":item.gender,
            "address":item.address,
            "branch_id":item.branch_id,
            "addharcard_number":item.addharcard_number,
            "pancard_number":item.pancard_number,
            "enabled":item.pancard_number,
            "enabled":item.enabled,
        } for item in customers_query
        ]
        return getResponse(True, customer_data,'Data get succesfully')
    except Exception as e :
        return getResponse(False, {"data": repr(e)})


@router.post("/add_customer",tags=['Customer'])
def addcustomer(
    customer_dict:CustomerBase,
    db:Session= Depends(getDB)
):
    try:
        customer_data=customer_dict.dict()
        
        check_user_exist = db.query(models.Customer).filter(
            or_(
                models.Customer.mobile_number == customer_data["mobile_number"],
                models.Customer.customer_email == customer_data["email"]
            )
        ).first()

        check_addhar_exist = db.query(models.Customer_adharcard_kyc).filter(
                models.Customer_adharcard_kyc.addharcard_number==customer_data["aadharcard"]
            ).first()
      

        check_pan_exist = db.query(models.CustomerPancardKyc).filter(
            models.CustomerPancardKyc.pancard_number==customer_data["pancard"]
         ).first()
     

        if check_user_exist or check_addhar_exist or check_pan_exist:
            return getResponse(False, '',"User Already Exist")
        
        new_data=models.Customer(
            customer_first_name=customer_data['first_name'],
            customer_last_name=customer_data['last_name'],
            customer_email=customer_data['email'],
            mobile_number=customer_data['mobile_number'],
            gender=customer_data['gender'],
            address=customer_data['address'],
            branch_id=customer_data['branch_id'],
        )
        db.add(new_data)
        db.flush()
        #    print(new_data.__dict__,"NEW")

        aadhar=models.Customer_adharcard_kyc(
            customer_id=new_data.customer_id,
            addharcard_number=customer_data['aadharcard']
        )

        pancard = models.CustomerPancardKyc(
            customer_id = new_data.customer_id,
            pancard_number = customer_data['pancard']
        )
        db.add_all([aadhar, pancard])
        db.commit()
        return getResponse(True,"Customer Added Succesfully")
    except Exception as e :
          db.rollback()
          return getResponse(False, {"data": repr(e)})
            

@router.post("/update_customer",tags=['Customer'])
def addcustomer(
    customer_updated_data:UpdateCustomerBase,
    db:Session= Depends(getDB)
):
    try:
       customer_data=customer_updated_data.dict()
       new_data=db.query(models.Customer).filter(models.Customer.customer_id==customer_data["customer_id"]).first()
       if new_data is None:
            getResponse(False, None,'Customer is Not Found')
       else:
            db.query(models.Customer).filter(models.Customer.customer_id==customer_data["customer_id"]).update(
                {
                    "customer_first_name":customer_data["first_name"],
                    "customer_last_name":customer_data["last_name"],
                    "customer_email":customer_data["email"],
                    "mobile_number":customer_data["mobile_number"],
                    "address":customer_data["address"],
                    "gender":customer_data["gender"]
                }
            )
            db.commit()
            db.query(models.Customer_adharcard_kyc).filter(models.Customer_adharcard_kyc.customer_id==customer_data["customer_id"]).update(
                {
                    "addharcard_number":customer_data["aadharcard"]
                }
               
            )
            db.commit()
            db.query(models.CustomerPancardKyc).filter(models.CustomerPancardKyc.customer_id==customer_data["customer_id"]).update(
                {
                    "pancard_number":customer_data["pancard"]
                }
               
            )
            db.commit()
            return getResponse(True, customer_data,"Customer Data Updated Succesfully")
    except Exception as e :
          return getResponse(False, {"data": repr(e)})

@router.post('/disabled_customer',tags=['Customer']) 
def disabledCustomer(
    customer_diabled:DisabledCustomer,
    db:Session = Depends(getDB)
):
    try:
        customerExits = db.query(models.Customer).filter(models.Customer.customer_id==customer_diabled.customer_id).first()
        print(customerExits,"customerExits")
        if customerExits is not None:
           db.query(models.Customer).filter(models.Customer.customer_id==customer_diabled.customer_id).update({
            "enabled" :False
           })
           db.commit()
           return getResponse(True,"Customer Disabled Succesfully")
        else:
            return getResponse(False,"Customer Not Found")
    except Exception as e :
        return getResponse(False, {"data": repr(e)})


@router.post('/enabled_customer',tags=['Customer'])
def enabledCustomer(
    customerDetails:DisabledCustomer,
    db:Session = Depends(getDB)
):
    try:
        userExits = db.query(models.Customer).filter(models.Customer.customer_id == customerDetails.customer_id).first()
        if userExits is not None:
            db.query(models.Customer).filter(models.Customer.customer_id == customerDetails.customer_id).update(
                {
                    "enabled":True
                }
            )
            db.commit()
            return getResponse(True,"Now User is Active ")
        else:
           return getResponse(False,"User Not Found")
    except Exception as e:
        return getResponse(False,{"data": repr(e)})
