from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.services.customer import CustomerService
from app.models.customer import CustomerCreate, CustomerRead, CustomerUpdate
from app.database import get_db
from app.logger import logger

router = APIRouter()

@router.post("/customers/", response_model=CustomerRead)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    service = CustomerService(db)
    return service.create_customer(customer)

@router.get("/customers/{customer_id}", response_model=CustomerRead)
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    service = CustomerService(db)
    return service.get_customer(customer_id)

@router.get("/customers/", response_model=list[CustomerRead])
def read_customers(db: Session = Depends(get_db)):
    service = CustomerService(db)
    return service.get_all_customers()

@router.patch("/customers/{customer_id}", response_model=CustomerRead)
def update_customer(customer_id: int, customer: CustomerUpdate, db: Session = Depends(get_db)):
    service = CustomerService(db)
    return service.update_customer(customer_id, customer)

@router.delete("/customers/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    service = CustomerService(db)
    service.delete_customer(customer_id)
    return {"message": "Customer deleted"}