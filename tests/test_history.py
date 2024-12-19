import pytest
from history.tracker import log_operation, fetch_history
from database.db import Base, engine, SessionLocal
from sqlalchemy.sql import text  # Import `text` for raw SQL

@pytest.fixture(scope="function", autouse=True)
def setup_database():
    """Fixture to set up the database for each test."""
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Clear data before each test
    db = SessionLocal()
    try:
        db.execute(text("DELETE FROM operation_history"))  # Wrap raw SQL in `text()`
        db.commit()
    finally:
        db.close()
    
    yield

    # Drop tables after each test
    Base.metadata.drop_all(bind=engine)

def test_log_operation():
    log_operation("add", [10, 20], 30)
    log_operation("multiply", [2, 5], 10)

    # Fetch history directly from the database
    history = fetch_history()

    assert len(history) == 2
    assert history[0] == "Add 10.0 and 20.0: Result = 30.0"
    assert history[1] == "Multiply 2.0 and 5.0: Result = 10.0"

def test_fetch_history():
    log_operation("divide", [100, 5], 20)
    log_operation("subtract", [50, 25], 25)

    history = fetch_history()

    assert len(history) == 2
    assert history[0] == "Divide 100.0 and 5.0: Result = 20.0"
    assert history[1] == "Subtract 50.0 and 25.0: Result = 25.0"

