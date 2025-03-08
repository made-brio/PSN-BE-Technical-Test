# Customer RESTful API Service

Customer RESTful API Service adalah aplikasi backend yang dibangun menggunakan **FastAPI** dan **SQLModel**. Aplikasi ini menyediakan endpoint untuk mengelola data pelanggan (customer) dan alamat (address) dengan menggunakan database **MariaDB/MySQL**.

## Fitur

- **CRUD Operations**:
  - Buat, baca, perbarui, dan hapus data pelanggan.
  - Buat, baca, perbarui, dan hapus data alamat.
- **Database Migrations**: Menggunakan **Alembic** untuk mengelola migrasi database.
- **Error Handling**: Custom exception handling untuk memberikan respons error yang informatif.
- **Logging**: Mencatat aktivitas aplikasi ke file log.
- **Docker Support**: Aplikasi dapat dijalankan menggunakan Docker.

## Teknologi yang Digunakan

- **Python 3.10**
- **FastAPI**: Framework untuk membangun API.
- **SQLModel**: Library untuk ORM dan validasi data.
- **MariaDB/MySQL**: Database untuk menyimpan data.
- **Alembic**: Library untuk migrasi database.
- **Docker**: Containerization untuk deployment.

## Cara Menjalankan Aplikasi

### 1. Prasyarat

- **Docker** dan **Docker Compose** terinstal di mesin Anda.
- **Python 3.10** (untuk development).

### 2. Setup Development

1. Clone repositori:
   ```bash
   git clone https://github.com/username/customer-api.git
   cd customer-api
   ```

2. Buat virtual environment dan install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Pada Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Buat file `.env` dan isi dengan konfigurasi yang sesuai:
   ```env
   DATABASE_URL=mysql+pymysql://user:password@localhost/customer_db
   LOG_LEVEL=INFO
   LOG_FILE=logs/app.log
   APP_NAME=Customer API
   APP_VERSION=1.0.0
   DEBUG=True
   ```

4. Inisialisasi migrasi database:
   ```bash
   python migrations.py init
   python migrations.py create "Initial migration"
   python migrations.py upgrade
   ```

5. Jalankan aplikasi:
   ```bash
   uvicorn app.main:app --reload
   ```

6. Akses aplikasi di `http://localhost:8000`.

### 3. Setup Production dengan Docker

1. Pastikan Docker dan Docker Compose sudah terinstal.

2. Buat file `.env` dan isi dengan konfigurasi yang sesuai:
   ```env
   DATABASE_URL=mysql+pymysql://user:password@db/customer_db
   LOG_LEVEL=INFO
   LOG_FILE=logs/app.log
   APP_NAME=Customer API
   APP_VERSION=1.0.0
   DEBUG=False
   ```

3. Build dan jalankan aplikasi menggunakan Docker Compose:
   ```bash
   docker-compose up --build
   ```

4. Akses aplikasi di `http://localhost:8000`.

### 4. Migrasi Database

- Untuk membuat migrasi baru:
  ```bash
  python migrations.py create "Deskripsi migrasi"
  ```

- Untuk menerapkan migrasi:
  ```bash
  python migrations.py upgrade
  ```

- Untuk rollback migrasi:
  ```bash
  python migrations.py downgrade
  ```

## Endpoint API

### Customer

- **GET /api/v1/customers/**: Mendapatkan daftar pelanggan.
- **GET /api/v1/customers/{customer_id}**: Mendapatkan detail pelanggan.
- **POST /api/v1/customers/**: Menambahkan pelanggan baru.
- **PATCH /api/v1/customers/{customer_id}**: Memperbarui data pelanggan.
- **DELETE /api/v1/customers/{customer_id}**: Menghapus pelanggan.

### Address

- **POST /api/v1/addresses/**: Menambahkan alamat baru.
- **PATCH /api/v1/addresses/{address_id}**: Memperbarui data alamat.
- **DELETE /api/v1/addresses/{address_id}**: Menghapus alamat.

## Testing

- Jalankan unit test dengan perintah:
  ```bash
  pytest app/tests
  ```