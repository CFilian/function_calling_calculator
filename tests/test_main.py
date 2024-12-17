from unittest.mock import MagicMock, patch
import groq_api.api as api  # Import the module under test

def test_call_groq_function():
    # Create a mock response to match the API structure
    mock_message = MagicMock()
    mock_message.content = "Test response"

    mock_choice = MagicMock()
    mock_choice.message = mock_message

    mock_response = MagicMock()
    mock_response.choices = [mock_choice]

    # Mock the client object and its behavior
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_response

    # Inject 'client' into the global namespace of api.py
    with patch.dict(api.__dict__, {"client": mock_client}):
        # Call the function under test
        user_input = "Hello, Groq!"
        result = api.call_groq_function(user_input)

        # Assertions
        mock_client.chat.completions.create.assert_called_once_with(
            messages=[{"role": "user", "content": user_input}],
            model="llama3-8b-8192",
        )
        assert result == "Test response"
