✅ sqlmodel = "^0.0.24" :
    =>What it is: A modern ORM (Object Relational Mapper) built on top of SQLAlchemy and Pydantic.

    =>Why it's used: To define database models and schemas in one place and interact with databases using Python classes.

    =>Usage: For creating tables, querying the database, and using models with FastAPI request/response.

✅ uvicorn = "^0.34.2" :
    =>What it is: A lightning-fast ASGI server used to run FastAPI apps.

    =>Why it's used: It serves your FastAPI application, supporting async features.

✅ pyjwt = "^2.10.1" :
    =>What it is: A Python library for creating and verifying JSON Web Tokens (JWTs).

    =>Why it's used: JWTs are used for authentication (e.g., when logging in).

    =>Usage: Encode user data into a token, then decode and validate that token later.

✅ python-multipart = "^0.0.20" :
    =>What it is: A library that enables FastAPI to parse multipart/form-data requests.

    =>Why it's used: Required for file uploads (e.g., images, PDFs).

    =>Usage: Needed if you're sending forms or uploading files from the frontend.

✅ python-dotenv = "^1.1.0" :
    =>What it is: Loads environment variables from a .env file.

    =>Why it's used: To keep sensitive settings (like SECRET_KEY, database URL) outside your code.

✅ loadenv = "^0.1.1":
    =>What it is: A helper tool to automatically load environment variables.

    =>Why it's used: Similar to python-dotenv; not always needed if you're already using dotenv.

✅ psycopg2 = "^2.9.10":
    =>What it is: A PostgreSQL adapter for Python.

    =>Why it's used: It allows your Python app to communicate with a PostgreSQL database.

    =>Usage: SQLModel/SQLAlchemy uses it under the hood to talk to PostgreSQL.

✅ bcrypt = "3.2.0":
    =>What it is: A password-hashing library.

    =>Why it's used: To securely hash user passwords before saving them to the database.

    =>Usage: Used by passlib under the hood to hash/check passwords.

✅ psycopg2-binary = "^2.9.10":
    =>What it is: A standalone binary distribution of psycopg2.

    =>Why it's used: Easier to install (no C compiler needed).

    Note: In production, it's better to use psycopg2 (non-binary) for performance and stability.


✅ passlib = "^1.7.4":
    =>What it is: A comprehensive password hashing library.

    =>Why it's used: To hash and verify passwords securely.

✅ python-jose = "^3.4.0":
    =>What it is: A library to handle JWTs and other security tokens (like pyjwt, but more advanced).

    =>Why it's used: For decoding and verifying JWTs in FastAPI apps.

✅ alembic = "^1.15.2":
    =>What it is: A database migration tool used with SQLAlchemy/SQLModel.

    =>Why it's used: To manage schema changes (e.g., adding tables or columns) without losing data.

    =>To set up the project with Alembic:

        poetry add alembic 

    =>Follow these steps to initialize Alembic and configure it for database migrations:

        poetry run alembic init alembic

    =>Whenever you make changes to your models, run the following commands:

        alembic revision --autogenerate -m "Add new table"
        alembic upgrade head
