from fastapi import status
from sqlmodel import Session

from app.models.customer import Customer

def test_create_customer(client, session: Session):
    # Data customer untuk testing
    customer_data = {
        "title": "Mr",
        "name": "John Doe",
        "gender": "M",
        "phone_number": "1234567890",
        "image": "https://example.com/image.jpg",
        "email": "john.doe@example.com"
    }

    # Kirim request POST ke endpoint /customers/
    response = client.post("/api/v1/customers/", json=customer_data)

    # Assert status code
    assert response.status_code == status.HTTP_200_OK

    # Assert data response
    data = response.json()
    assert data["name"] == customer_data["name"]
    assert data["email"] == customer_data["email"]
    assert "id" in data

    # Verifikasi data di database
    db_customer = session.get(Customer, data["id"])
    assert db_customer is not None
    assert db_customer.name == customer_data["name"]

def test_read_customers(client, session: Session):
    # Buat data customer di database
    customer1 = Customer(
        title="Mr",
        name="John Doe",
        gender="M",
        phone_number="1234567890",
        image="https://example.com/image.jpg",
        email="john.doe@example.com"
    )
    customer2 = Customer(
        title="Ms",
        name="Jane Doe",
        gender="F",
        phone_number="0987654321",
        image="https://example.com/image2.jpg",
        email="jane.doe@example.com"
    )
    session.add(customer1)
    session.add(customer2)
    session.commit()

    # Kirim request GET ke endpoint /customers/
    response = client.get("/api/v1/customers/")

    # Assert status code
    assert response.status_code == status.HTTP_200_OK

    # Assert data response
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "John Doe"
    assert data[1]["name"] == "Jane Doe"

def test_read_customer(client, session: Session):
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

    # Kirim request GET ke endpoint /customers/{customer_id}
    response = client.get(f"/api/v1/customers/{customer.id}")

    # Assert status code
    assert response.status_code == status.HTTP_200_OK

    # Assert data response
    data = response.json()
    assert data["name"] == "John Doe"
    assert data["email"] == "john.doe@example.com"

def test_update_customer(client, session: Session):
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

    # Data update
    update_data = {"name": "John Updated"}

    # Kirim request PATCH ke endpoint /customers/{customer_id}
    response = client.patch(f"/api/v1/customers/{customer.id}", json=update_data)

    # Assert status code
    assert response.status_code == status.HTTP_200_OK

    # Assert data response
    data = response.json()
    assert data["name"] == "John Updated"

    # Verifikasi data di database
    db_customer = session.get(Customer, customer.id)
    assert db_customer.name == "John Updated"

def test_delete_customer(client, session: Session):
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

    # Kirim request DELETE ke endpoint /customers/{customer_id}
    response = client.delete(f"/api/v1/customers/{customer.id}")

    # Assert status code
    assert response.status_code == status.HTTP_200_OK

    # Verifikasi data di database
    db_customer = session.get(Customer, customer.id)
    assert db_customer is None