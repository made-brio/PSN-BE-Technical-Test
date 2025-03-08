from sqlmodel import Session
from app.repositories.customer import CustomerRepository
from app.models.customer import Customer, CustomerCreate, CustomerUpdate
from app.exceptions.handlers import NotFoundException, BadRequestException
from app.logger import logger

class CustomerService:
    def __init__(self, session: Session):
        self.repository = CustomerRepository(session)

    def create_customer(self, customer: CustomerCreate):
        logger.info(f"Creating customer: {customer.name}")
        return self.repository.create(customer)

    def get_customer(self, customer_id: int):
        logger.info(f"Fetching customer with ID: {customer_id}")
        customer = self.repository.get(customer_id)
        if not customer:
            logger.warning(f"Customer with ID {customer_id} not found")
            raise NotFoundException(detail="Customer not found")
        return customer
    
    def get_all_customers(self):
        logger.info("Fetching all customers")
        return self.repository.get_all()

    def update_customer(self, customer_id: int, customer: CustomerUpdate):
        logger.info(f"Updating customer with ID: {customer_id}")
        db_customer = self.repository.get(customer_id)
        if not db_customer:
            logger.warning(f"Customer with ID {customer_id} not found")
            raise NotFoundException(detail="Customer not found")
        return self.repository.update(customer_id, customer)

    def delete_customer(self, customer_id: int):
        logger.info(f"Deleting customer with ID: {customer_id}")
        db_customer = self.repository.get(customer_id)
        if not db_customer:
            logger.warning(f"Customer with ID {customer_id} not found")
            raise NotFoundException(detail="Customer not found")
        self.repository.delete(customer_id)