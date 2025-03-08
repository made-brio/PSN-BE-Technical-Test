from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.v1.endpoints import customer, address
from app.config import settings
from app.database import engine
from app.models.customer import Customer
from app.models.address import Address
from app.exceptions.handlers import add_exception_handlers
from app.logger import logger

Customer.metadata.create_all(engine)
Address.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application started")
    yield
    logger.info("Application shutdown")

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION, debug=settings.DEBUG, lifespan=lifespan)

add_exception_handlers(app)

app.include_router(customer.router, prefix="/api/v1")
app.include_router(address.router, prefix="/api/v1")