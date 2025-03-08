from sqlmodel import Session
from app.models.address import Address, AddressCreate, AddressUpdate

class AddressRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, address: AddressCreate):
        db_address = Address(**address.model_dump())
        self.session.add(db_address)
        self.session.commit()
        self.session.refresh(db_address)
        return db_address

    def get(self, address_id: int):
        return self.session.get(Address, address_id)

    def update(self, address_id: int, address: AddressUpdate):
        db_address = self.session.get(Address, address_id)
        if db_address:
            for key, value in address.model_dump(exclude_unset=True).items():
                setattr(db_address, key, value)
            self.session.commit()
            self.session.refresh(db_address)
        return db_address

    def delete(self, address_id: int):
        db_address = self.session.get(Address, address_id)
        if db_address:
            self.session.delete(db_address)
            self.session.commit()
        return db_address