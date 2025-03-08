from fastapi import status
from sqlmodel import Session

from app.models.customer import Customer
from app.models.address import Address

def test_create_address(client, session: Session):
    # Buat data customer di database
    customer = Customer(
        title="Mr",
        name="John Doe",
        gender="M",
        phone_number="1234567890",
        image="https://example.com/image.jpg",
        email="john.doe@example.com"
    )
    session.add(customer)
    session.commit()

    # Data address untuk testing
    address_data = {
        "address": "123 Main St",
        "district": "Central",
        "city": "Metropolis",
        "province": "Superstate",
        "postal_code": 12345,
        "customer_id": customer.id
    }

    # Kirim request POST ke endpoint /addresses/
    response = client.post("/api/v1/addresses/", json=address_data)

    # Assert status code
    assert response.status_code == status.HTTP_200_OK

    # Assert data response
    data = response.json()
    assert data["address"] == address_data["address"]
    assert data["customer_id"] == customer.id
    assert "id" in data

    # Verifikasi data di database
    db_address = session.get(Address, data["id"])
    assert db_address is not None
    assert db_address.address == address_data["address"]

def test_update_address(client, session: Session):
    # Buat data customer dan address di database
    customer = Customer(
        title="Mr",
        name="John Doe",
        gender="M",
        phone_number="1234567890",
        image="https://example.com/image.jpg",
        email="john.doe@example.com"
    )
    session.add(customer)
    session.commit()

    address = Address(
        address="123 Main St",
        district="Central",
        city="Metropolis",
        province="Superstate",
        postal_code=12345,
        customer_id=customer.id
    )
    session.add(address)
    session.commit()

    # Data update
    update_data = {"address": "456 Updated St"}

    # Kirim request PATCH ke endpoint /addresses/{address_id}
    response = client.patch(f"/api/v1/addresses/{address.id}", json=update_data)

    # Assert status code
    assert response.status_code == status.HTTP_200_OK

    # Assert data response
    data = response.json()
    assert data["address"] == "456 Updated St"

    # Verifikasi data di database
    db_address = session.get(Address, address.id)
    assert db_address.address == "456 Updated St"

def test_delete_address(client, session: Session):
    # Buat data customer dan address di database
    customer = Customer(
        title="Mr",
        name="John Doe",
        gender="M",
        phone_number="1234567890",
        image="https://example.com/image.jpg",
        email="john.doe@example.com"
    )
    session.add(customer)
    session.commit()

    address = Address(
        address="123 Main St",
        district="Central",
        city="Metropolis",
        province="Superstate",
        postal_code=12345,
        customer_id=customer.id
    )
    session.add(address)
    session.commit()

    # Kirim request DELETE ke endpoint /addresses/{address_id}
    response = client.delete(f"/api/v1/addresses/{address.id}")

    # Assert status code
    assert response.status_code == status.HTTP_200_OK

    # Verifikasi data di database
    db_address = session.get(Address, address.id)
    assert db_address is None