from sqlmodel import Session, select
from app.models.customer import Customer, CustomerCreate, CustomerUpdate

class CustomerRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, customer: CustomerCreate):
        db_customer = Customer(**customer.model_dump())
        self.session.add(db_customer)
        self.session.commit()
        self.session.refresh(db_customer)
        return db_customer

    def get(self, customer_id: int):
        return self.session.get(Customer, customer_id)

    def get_all(self):
        return self.session.exec(select(Customer)).all()

    def update(self, customer_id: int, customer: CustomerUpdate):
        db_customer = self.session.get(Customer, customer_id)
        if db_customer:
            for key, value in customer.model_dump(exclude_unset=True).items():
                setattr(db_customer, key, value)
            self.session.commit()
            self.session.refresh(db_customer)
        return db_customer

    def delete(self, customer_id: int):
        db_customer = self.session.get(Customer, customer_id)
        if db_customer:
            self.session.delete(db_customer)
            self.session.commit()
        return db_customer