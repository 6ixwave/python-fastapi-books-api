from app.db import models  # noqa: F401
from app.db.db import create_tables


if __name__ == "__main__":
    create_tables()
    print("Database tables are ready.")
