import os
from alembic import command
from alembic.config import Config
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Path ke direktori migrations
MIGRATIONS_DIR = "alembic"

def init_migrations():
    """Inisialisasi direktori migrations."""
    if os.path.exists(MIGRATIONS_DIR):
        if os.listdir(MIGRATIONS_DIR):
            raise Exception(f"Directory '{MIGRATIONS_DIR}' is not empty. Please remove it first.")
    else:
        os.makedirs(MIGRATIONS_DIR)

    # Inisialisasi Alembic
    alembic_cfg = Config("alembic.ini")
    command.init(alembic_cfg, MIGRATIONS_DIR)

    # Update file alembic.ini
    alembic_ini_path = "alembic.ini"
    with open(alembic_ini_path, "r") as f:
        content = f.read()

    # Ganti sqlalchemy.url dengan URL database
    content = content.replace(
        "sqlalchemy.url = driver://user:pass@localhost/dbname",
        f"sqlalchemy.url = {SQLALCHEMY_DATABASE_URL}"
    )

    with open(alembic_ini_path, "w") as f:
        f.write(content)

    # Update file env.py
    env_py_path = os.path.join(MIGRATIONS_DIR, "env.py")
    with open(env_py_path, "r") as f:
        content = f.read()

    # Ganti target_metadata dengan SQLModel.metadata
    content = content.replace(
        "target_metadata = None",
        f"""
from sqlmodel import SQLModel
from app.models.address import Address
from app.models.customer import Customer
target_metadata = SQLModel.metadata
        """
    )

    with open(env_py_path, "w") as f:
        f.write(content)

    # Update file script.py.mako untuk menyertakan import sqlmodel
    script_mako_path = os.path.join(MIGRATIONS_DIR, "script.py.mako")
    with open(script_mako_path, "r") as f:
        content = f.read()

    # Tambahkan import sqlmodel ke dalam template
    content = content.replace(
        "${imports if imports else \"\"}",
        "import sqlmodel\n${imports if imports else \"\"}"
    )

    with open(script_mako_path, "w") as f:
        f.write(content)

    # Buat migrasi awal
    create_revision("Initial migration")

def create_revision(message: str):
    """Buat revisi migrasi baru."""
    alembic_cfg = Config("alembic.ini")
    command.revision(alembic_cfg, autogenerate=True, message=message)

def upgrade_migrations(revision: str = "head"):
    """Terapkan migrasi ke database."""
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, revision)

def downgrade_migrations(revision: str = "base"):
    """Rollback migrasi."""
    alembic_cfg = Config("alembic.ini")
    command.downgrade(alembic_cfg, revision)

def show_current():
    """Tampilkan revisi migrasi saat ini."""
    alembic_cfg = Config("alembic.ini")
    command.current(alembic_cfg)

def show_history():
    """Tampilkan history migrasi."""
    alembic_cfg = Config("alembic.ini")
    command.history(alembic_cfg)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Manage database migrations.")
    subparsers = parser.add_subparsers(dest="command")

    # Subcommand: init
    init_parser = subparsers.add_parser("init", help="Initialize migrations directory.")

    # Subcommand: create
    create_parser = subparsers.add_parser("create", help="Create a new migration revision.")
    create_parser.add_argument("message", type=str, help="Message for the migration.")

    # Subcommand: upgrade
    upgrade_parser = subparsers.add_parser("upgrade", help="Upgrade the database.")
    upgrade_parser.add_argument("--revision", type=str, default="head", help="Target revision.")

    # Subcommand: downgrade
    downgrade_parser = subparsers.add_parser("downgrade", help="Downgrade the database.")
    downgrade_parser.add_argument("--revision", type=str, default="base", help="Target revision.")

    # Subcommand: current
    subparsers.add_parser("current", help="Show the current revision.")

    # Subcommand: history
    subparsers.add_parser("history", help="Show migration history.")

    args = parser.parse_args()

    if args.command == "init":
        init_migrations()
    elif args.command == "create":
        create_revision(args.message)
    elif args.command == "upgrade":
        upgrade_migrations(args.revision)
    elif args.command == "downgrade":
        downgrade_migrations(args.revision)
    elif args.command == "current":
        show_current()
    elif args.command == "history":
        show_history()
    else:
        parser.print_help()