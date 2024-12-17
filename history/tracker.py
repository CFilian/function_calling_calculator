import datetime

LOG_FILE = "operation_history.log"

def log_operation(message):
    """
    Logs a message to both the console and a log file.

    Args:
        message (str): The message to log.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {message}"

    # Log to the console
    print(log_message)

    # Append the message to a log file
    with open(LOG_FILE, "a") as file:
        file.write(log_message + "\n")
