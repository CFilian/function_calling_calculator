from groq_api.api import call_groq_function
from history.tracker import History
from arithmetic.operations import add, subtract, multiply, divide

def console_chat():
    history = History()
    print("Welcome to the Groq Function Chat!")
    print("You can ask the system to perform addition, subtraction, multiplication, or division.")
    print("Type 'history' to view your past calculations.")
    print("Type 'quit' to exit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            print("Goodbye!")
            break

        if user_input.lower() == "history":
            print("\nCalculation History:")
            for record in history.get_all():
                print(record)
            continue

        try:
            result = call_groq_function(user_input)
            if result is not None:
                print(f"Result: {result}")
                history.add_entry(user_input, result)
            else:
                print("No function call was made or an error occurred.")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    console_chat()
