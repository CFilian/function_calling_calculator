from flask import Flask, request, jsonify, render_template_string
from arithmetic.operations import add, subtract, multiply, divide
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
    <div id="output">Welcome to the Function Calling Calculator!\nTo use commands use  'add', 'subtract ', 'multiply ', or 'divide '.\nFunction can be used as is:\n'operation' num(space)num\n'operation' num(+,*,/,-)num\n'operation' num(space)(+,*,/,-)(space)num\nType 'quit' to exit.\n</div>
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

                // Send the command to the Flask server
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
    Parse a command string like 'add 10 + 20' or 'multiply 5*6' and return operation and numbers.

    Args:
        command (str): The user input string.

    Returns:
        tuple: (operation, num1, num2) or raises ValueError if invalid.
    """
    try:
        # Extract operation and numbers using regex
        match = re.match(r"(\w+)\s*(\d+)\s*[\+\-\*\/]?\s*(\d+)", command)
        if not match:
            raise ValueError("Invalid command format. Use 'add 10+20' or similar.")
        
        operation = match.group(1).lower()
        num1 = int(match.group(2))
        num2 = int(match.group(3))

        return operation, num1, num2
    except Exception:
        raise ValueError("Failed to parse the command. Use 'add 10+20' or similar.")

@app.route("/execute", methods=["POST"])
def execute_command():
    """Process user commands and perform operations."""
    data = request.get_json()
    command = data.get("command", "")
    response_message = ""

    try:
        operation, num1, num2 = parse_command(command)

        if operation == "add":
            result = add(num1, num2)
        elif operation == "subtract":
            result = subtract(num1, num2)
        elif operation == "multiply":
            result = multiply(num1, num2)
        elif operation == "divide":
            if num2 == 0:
                raise ValueError("Error: Division by zero is not allowed.")
            result = divide(num1, num2)
        else:
            raise ValueError("Unsupported operation. Use add, subtract, multiply, or divide.")

        log_operation(f"{operation.title()} {num1} and {num2}: Result = {result}")
        response_message = f"Result: {result}"
    except Exception as e:
        response_message = f"Error: {str(e)}"

    return jsonify({"message": response_message})

if __name__ == "__main__":
    # Run the Flask app
    app.run(host="0.0.0.0", port=8000)
