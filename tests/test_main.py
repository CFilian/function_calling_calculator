from unittest.mock import patch
from groq_api.api import call_groq_function

@patch("groq_api.api.client.chat.completions.create")
def test_call_groq_function(mock_create):
    # Mock the Groq API response as a dictionary
    mock_create.return_value = {
        "choices": [
            {"message": {"content": "Mocked Response"}}
        ]
    }

    # Call the function with mocked response
    result = call_groq_function("Test input")
    
    # Assertions
    assert result == "Mocked Response"

    # Ensure the mock was called with the correct arguments
    mock_create.assert_called_once_with(
        messages=[{"role": "user", "content": "Test input"}],
        model="llama3-8b-8192",
    )
