from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime

class AddressBase(SQLModel):
    address: str
    district: str
    city: str
    province: str
    postal_code: int
    customer_id: int = Field(foreign_key="customer.id")

class Address(AddressBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    customer: "Customer" = Relationship(back_populates="addresses")

class AddressCreate(AddressBase):
    pass

class AddressRead(AddressBase):
    id: int
    created_at: datetime
    updated_at: datetime

class AddressUpdate(SQLModel):
    address: str | None = None
    district: str | None = None
    city: str | None = None
    province: str | None = None
    postal_code: int | None = None
    customer_id: int | None = None