from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./calculator.db"  # Use SQLite for simplicity

# Create the database engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Configure session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define the base class for models
Base = declarative_base()
