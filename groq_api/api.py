import groq  # Import the Groq SDK

# Initialize the client with your API key
client = groq.Groq(api_key="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")  # Replace with your actual Groq API key

def call_groq_function(user_input):
    """
    Calls the Groq API to process the user input and return the result.
    """
    if not client:
        raise EnvironmentError("Groq client is not properly initialized.")

    try:
        # Send a chat completion request
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": user_input,
                }
            ],
            model="llama3-8b-8192",  # Adjust the model name based on your API access
        )

        # Access the response as a dictionary
        return chat_completion.choices[0].message.content  # Access properties safely

    except Exception as e:
        raise RuntimeError(f"An error occurred: {e}")

# Example usage
try:
    response = call_groq_function("Tell me a joke about AI.")
    print("Groq Response:", response)
except Exception as err:
    print(err)
