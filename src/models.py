from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey,  Integer, String, Text,  func
from src.database import Base


class Role(Base):
    __tablename__='mst_role'
    role_id = Column(Integer,nullable=False,primary_key=True,index=True,autoincrement=True)
    role_name = Column(String,nullable=False)
    created_at = Column(DateTime(timezone=False),nullable=False,server_default=func.current_timestamp(),)
    updated_at = Column(DateTime, nullable=True,onupdate=func.current_timestamp())

class Branch(Base):
    __tablename__='mst_branch'
    branch_id = Column(Integer,nullable=False,primary_key=True,index=True,autoincrement=True)
    branch_name = Column(String,nullable=False)
    branch_location = Column(String,nullable=False)
    created_at = Column(DateTime(timezone=False),nullable=False,server_default=func.current_timestamp(),)
    updated_at = Column(DateTime, nullable=True,onupdate=func.current_timestamp())
    created_by = Column(Integer, ForeignKey("mst_user.user_id"), nullable=True)
    updated_by = Column(Integer, ForeignKey("mst_user.user_id"), nullable=True)

class User(Base):
    __tablename__ = "mst_user"
    user_id = Column(
        Integer, nullable=False, primary_key=True, index=True, autoincrement=True
    )
    role_id = Column(Integer, ForeignKey("mst_role.role_id"),nullable=False)
    branch_id = Column(Integer, ForeignKey("mst_branch.branch_id"),nullable=False)
    user_name = Column(Text, nullable=False)
    user_email = Column(Text, nullable=False, unique=True)
    manager_id = Column(Integer, ForeignKey("mst_user.user_id"), nullable=True)
    mobile_number = Column(Text, nullable=False)
    enabled = Column(Boolean, nullable=False, default=True)
    created_by = Column(Integer, ForeignKey("mst_user.user_id"), nullable=True)
    created_at = Column(
        DateTime(timezone=False),
        nullable=False,
        server_default=func.current_timestamp(),
    )
    updated_at = Column(DateTime, nullable=True,
                        onupdate=func.current_timestamp())
    updated_by = Column(Integer, ForeignKey("mst_user.user_id"), nullable=True)

    
class Customer(Base):
    __tablename__='mst_customer'
    customer_id = Column(
        Integer, nullable=False, primary_key=True, index=True, autoincrement=True
    )
    branch_id = Column(Integer, ForeignKey("mst_branch.branch_id"),nullable=False)
    customer_first_name = Column(Text, nullable=False)
    customer_last_name = Column(Text, nullable=False)
    customer_email = Column(Text, nullable=False, unique=True)
    manager_id = Column(Integer, ForeignKey("mst_user.user_id"), nullable=True)
    mobile_number = Column(Text, nullable=True)
    address = Column(Text, nullable=True)
    gender = Column(Text, nullable=True)
    enabled = Column(Boolean, nullable=False, default=True)
    created_by = Column(Integer, ForeignKey("mst_user.user_id"), nullable=True)
    created_at = Column(
        DateTime(timezone=False),
        nullable=False,
        server_default=func.current_timestamp(),
    )
    updated_at = Column(DateTime, nullable=True,
                        onupdate=func.current_timestamp())
    updated_by = Column(Integer, ForeignKey("mst_user.user_id"), nullable=True)


class Customer_adharcard_kyc(Base):
    __tablename__='mst_aadhar_kyc'
    addharcard_id=Column(Integer,primary_key=True,nullable=False,autoincrement=True)
    customer_id=Column(Integer,ForeignKey("mst_customer.customer_id"),nullable=False)
    addharcard_number=Column(Text,nullable=False)
    created_by = Column(Integer, ForeignKey("mst_user.user_id"), nullable=True)
    created_at = Column(
        DateTime(timezone=False),
        nullable=False,
        server_default=func.current_timestamp(),
    )
    updated_at = Column(DateTime, nullable=True,
                        onupdate=func.current_timestamp())
    updated_by = Column(Integer, ForeignKey("mst_user.user_id"), nullable=True)


class CustomerPancardKyc(Base):
    __tablename__='mst_pancard_kyc'
    pancard_id=Column(Integer,primary_key=True,nullable=False,autoincrement=True)
    customer_id=Column(Integer,ForeignKey("mst_customer.customer_id"),nullable=False)
    pancard_number=Column(Text,nullable=False)
    created_by = Column(Integer, ForeignKey("mst_user.user_id"), nullable=True)
    created_at = Column(
        DateTime(timezone=False),
        nullable=False,
        server_default=func.current_timestamp(),
    )
    updated_at = Column(DateTime, nullable=True,
                        onupdate=func.current_timestamp())
    updated_by = Column(Integer, ForeignKey("mst_user.user_id"), nullable=True)


class Customer_votingcard_kyc(Base):
    __tablename__='mst_voting_kyc'
    voting_id=Column(Integer,primary_key=True,nullable=False,autoincrement=True)
    customer_id=Column(Integer,ForeignKey("mst_customer.customer_id"),nullable=False)
    voting_number=Column(Text,nullable=False)
    created_by = Column(Integer, ForeignKey("mst_user.user_id"), nullable=True)
    created_at = Column(
        DateTime(timezone=False),
        nullable=False,
        server_default=func.current_timestamp(),
    )
    updated_at = Column(DateTime, nullable=True,
                        onupdate=func.current_timestamp())
    updated_by = Column(Integer, ForeignKey("mst_user.user_id"), nullable=True)

class Account(Base):
    __tablename__='mst_account'
    account_id=Column(Integer,primary_key=True,nullable=False,autoincrement=True)
    customer_id=Column(Integer,ForeignKey("mst_customer.customer_id"),nullable=False)
    account_type_id=Column(Integer,ForeignKey("mst_account_type.account_type_id"))
    balance=Column(Float,nullable=False)
    created_by = Column(Integer, ForeignKey("mst_user.user_id"), nullable=True)
    created_at = Column(
        DateTime(timezone=False),
        nullable=False,
        server_default=func.current_timestamp(),
    )


class Account_type(Base):
    __tablename__='mst_account_type'
    account_type_id=Column(Integer,primary_key=True,nullable=False,autoincrement=True)
    account_type_name=Column(Text,nullable=False)

class loan_type(Base):
    __tablename__='mst_loan_type'
    loan_type_id=Column(Integer,primary_key=True,nullable=False,autoincrement=True)
    loan_type_name=Column(Text,nullable=False)

class transaction_type(Base):
    __tablename__='mst_transaction_type'
    transaction_type_id=Column(Integer,primary_key=True,nullable=False,autoincrement=True)
    transaction_type_name=Column(Text,nullable=False)

class loan(Base):
    __tablename__='mst_loan'
    loan_id = Column(Integer,primary_key=True,nullable=False,autoincrement=True)
    loan_type_id = Column(Integer,ForeignKey('mst_loan_type.loan_type_id'),nullable=False)
    customer_id=Column(Integer,ForeignKey('mst_customer.customer_id'),nullable=False)
    loan_amount=Column(Float,nullable=False)
    intrest_rate=Column(Float,nullable=False)
    loan_start_date=Column(DateTime,nullable=False)
    loan_end_date=Column(DateTime,nullable=False)
    created_by = Column(Integer, ForeignKey("mst_user.user_id"), nullable=True)
    created_at = Column(DateTime(timezone=False),nullable=False,server_default=func.current_timestamp(),)
   

class transaction(Base):
     __tablename__='mst_transaction'
     transaction_id=Column(Integer,primary_key=True,nullable=False,autoincrement=True)
     account_id=Column(Integer,ForeignKey('mst_account.account_id'),nullable=False)
     transaction_type_id = Column(Integer,ForeignKey('mst_transaction_type.transaction_type_id'),nullable=False)
     amount=Column(Float,nullable=False)
     transaction_date=Column(DateTime,nullable=False)




