from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime

class CustomerBase(SQLModel):
    title: str
    name: str = Field(index=True)
    gender: str
    phone_number: str
    image: str
    email: str = Field(index=True)

class Customer(CustomerBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    addresses: List["Address"] = Relationship(back_populates="customer")

class CustomerCreate(CustomerBase):
    pass

class CustomerRead(CustomerBase):
    id: int
    created_at: datetime
    updated_at: datetime

class CustomerUpdate(SQLModel):
    title: str | None = None
    name: str | None = None
    gender: str | None = None
    phone_number: str | None = None
    image: str | None = None
    email: str | None = None