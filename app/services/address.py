from sqlmodel import Session
from app.repositories.address import AddressRepository
from app.models.address import Address, AddressCreate, AddressUpdate
from app.exceptions.handlers import NotFoundException, BadRequestException
from app.logger import logger

class AddressService:
    def __init__(self, session: Session):
        self.repository = AddressRepository(session)

    def create_address(self, address: AddressCreate):
        logger.info(f"Creating address for customer ID: {address.customer_id}")
        return self.repository.create(address)

    def get_address(self, address_id: int):
        logger.info(f"Fetching address with ID: {address_id}")
        address = self.repository.get(address_id)
        if not address:
            logger.warning(f"Address with ID {address_id} not found")
            raise NotFoundException(detail="Address not found")
        return address

    def update_address(self, address_id: int, address: AddressUpdate):
        logger.info(f"Updating address with ID: {address_id}")
        db_address = self.repository.get(address_id)
        if not db_address:
            logger.warning(f"Address with ID {address_id} not found")
            raise NotFoundException(detail="Address not found")
        return self.repository.update(address_id, address)

    def delete_address(self, address_id: int):
        logger.info(f"Deleting address with ID: {address_id}")
        db_address = self.repository.get(address_id)
        if not db_address:
            logger.warning(f"Address with ID {address_id} not found")
            raise NotFoundException(detail="Address not found")
        self.repository.delete(address_id)