from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.services.address import AddressService
from app.models.address import AddressCreate, AddressRead, AddressUpdate
from app.database import get_db
from app.logger import logger

router = APIRouter()

@router.post("/addresses/", response_model=AddressRead)
def create_address(address: AddressCreate, db: Session = Depends(get_db)):
    service = AddressService(db)
    return service.create_address(address)

@router.get("/addresses/{address_id}", response_model=AddressRead)
def read_address(address_id: int, db: Session = Depends(get_db)):
    service = AddressService(db)
    return service.get_address(address_id)

@router.patch("/addresses/{address_id}", response_model=AddressRead)
def update_address(address_id: int, address: AddressUpdate, db: Session = Depends(get_db)):
    service = AddressService(db)
    return service.update_address(address_id, address)

@router.delete("/addresses/{address_id}")
def delete_address(address_id: int, db: Session = Depends(get_db)):
    service = AddressService(db)
    service.delete_address(address_id)
    return {"message": "Address deleted"}