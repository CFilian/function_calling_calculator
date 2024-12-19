import datetime
from sqlalchemy.orm import Session
from database.db import SessionLocal
from database.models import OperationHistory

LOG_FILE = "operation_history.log"

def log_operation(operation, operands, result):
    """
    Logs an operation to the console, a log file, and the database.

    Args:
        operation (str): The operation performed (e.g., add, subtract).
        operands (list[float]): List of operands used in the operation.
        result (float): The result of the operation.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    operands_str = " and ".join(map(str, operands))
    log_message = f"[{timestamp}] {operation.title()} {operands_str}: Result = {result}"

    # Log to the console
    print(log_message)

    # Append the message to a log file
    with open(LOG_FILE, "a") as file:
        file.write(log_message + "\n")

    # Log to the database
    db = SessionLocal()
    try:
        for i in range(len(operands) - 1):
            new_entry = OperationHistory(
                operation=operation,
                operand1=operands[i],
                operand2=operands[i + 1],
                result=result
            )
            db.add(new_entry)
        db.commit()
    except Exception as e:
        print(f"Error logging to database: {e}")
    finally:
        db.close()

def fetch_history():
    """
    Fetches operation history from the database.

    Returns:
        list[str]: List of logged operations as strings.
    """
    db = SessionLocal()
    history = []
    try:
        entries = db.query(OperationHistory).all()
        for entry in entries:
            history.append(
                f"{entry.operation.title()} {entry.operand1} and {entry.operand2}: Result = {entry.result}"
            )
    except Exception as e:
        print(f"Error fetching history from database: {e}")
    finally:
        db.close()
    return history
