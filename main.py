from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src import database, models
from src.project.users_router import router as users_routes
from src.project.branch_router import router as branch_router
from src.project.customer_router import router as customer_router
from src.project.loan_router import router as loan_router
app = FastAPI()


models.Base.metadata.create_all(bind=database.engine)


origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


list_of_routers = [users_routes,branch_router,customer_router,loan_router]


for routes in list_of_routers:
    app.include_router(routes)

