from flask import Flask, request, jsonify, render_template_string
from arithmetic.operations import add, subtract, multiply, divide
from database.db import Base, engine, SessionLocal
from database.models import OperationHistory
from history.tracker import log_operation
import re  # For parsing the input

# Create Flask app instance
app = Flask(__name__)

# HTML Template for the web terminal
HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Web CLI</title>
    <style>
        body { background-color: black; color: lime; font-family: monospace; padding: 20px; }
        #output { white-space: pre-wrap; margin-bottom: 10px; height: 400px; overflow-y: auto; }
        input { background-color: black; color: lime; border: none; width: 100%; outline: none; font-family: monospace; }
        input:focus { outline: none; }
    </style>
</head>
<body>
    <div id="output">Welcome to the Function Calling Calculator!\nTo use commands use 'add', 'subtract', 'multiply', or 'divide'.\nExample usage:\n'operation num1 num2'\nType 'history' to view past calculations.\nType 'quit' to exit.\n</div>
    <input id="input" autofocus placeholder="Type a command..." />

    <script>
        const inputField = document.getElementById("input");
        const outputDiv = document.getElementById("output");

        inputField.addEventListener("keydown", async (event) => {
            if (event.key === "Enter") {
                const command = inputField.value;
                outputDiv.textContent += "> " + command + "\\n";
                inputField.value = "";

                if (command.toLowerCase() === "quit") {
                    outputDiv.textContent += "Exiting...\\n";
                    return;
                }

                const response = await fetch("/execute", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ command })
                });
                const data = await response.json();
                outputDiv.textContent += data.message + "\\n";
                outputDiv.scrollTop = outputDiv.scrollHeight;
            }
        });
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    """Serve the web-based CLI interface."""
    return render_template_string(HTML_PAGE)

def parse_command(command):
    """
    Parse a command string like 'add 10 20' or '10 + 20' and return operation and numbers.

    Args:
        command (str): The user input string.

    Returns:
        tuple: (operation, numbers) or raises ValueError if invalid.
    """
    try:
        # Handle commands with operators like "+" or "*"
        if any(op in command for op in ["+", "-", "*", "/"]):
            match = re.split(r"([+\-*/])", command.replace(" ", ""))
            if not match or len(match) < 3:
                raise ValueError("Invalid command format. Use '10 + 20' or 'add 10 20'.")
            
            operation = "add" if "+" in match else "subtract" if "-" in match else "multiply" if "*" in match else "divide"
            numbers = [float(num) for num in match if num.strip() and num not in "+-*/"]
        else:
            # Handle commands like 'add 10 20'
            match = re.match(r"(\w+)\s+([\d\s\.]+)", command)
            if not match:
                raise ValueError("Invalid command format. Use 'add 10 20'.")
            
            operation = match.group(1).lower()
            numbers = [float(num) for num in match.group(2).split()]
        return operation, numbers
    except Exception:
        raise ValueError("Failed to parse the command. Use '10 + 20' or 'add 10 20'.")

@app.route("/execute", methods=["POST"])
def execute_command():
    """Process user commands and perform operations."""
    data = request.get_json()
    command = data.get("command", "").strip()
    response_message = ""

    try:
        if command.lower() == "history":
            # Fetch history of calculations from the database using ORM
            db = SessionLocal()
            results = db.query(OperationHistory).all()
            db.close()

            if not results:
                response_message = "No calculations in history."
            else:
                response_message = "Calculation History:\n" + "\n".join(
                    [f"{row.operation.title()} {row.operand1} and {row.operand2}: Result = {row.result}" for row in results]
                )
        else:
            # Parse the command
            operation, numbers = parse_command(command)

            # Perform the operation
            if operation == "add":
                result = round(sum(numbers), 2)
            elif operation == "subtract":
                result = round(numbers[0] - sum(numbers[1:]), 2)
            elif operation == "multiply":
                result = round(eval('*'.join(map(str, numbers))), 2)
            elif operation == "divide":
                result = numbers[0]
                for num in numbers[1:]:
                    if num == 0:
                        raise ValueError("Division by zero is not allowed.")
                    result /= num
                result = round(result, 2)
            else:
                raise ValueError("Unsupported operation. Use add, subtract, multiply, or divide.")

            # Log the operation to the database
            log_operation(operation, numbers, result)
            response_message = f"Result: {result}"
    except Exception as e:
        response_message = f"Error: {str(e)}"

    return jsonify({"message": response_message})

if __name__ == "__main__":
    # Initialize the database
    Base.metadata.create_all(bind=engine)

    # Run the Flask app
    app.run(host="0.0.0.0", port=8000)
