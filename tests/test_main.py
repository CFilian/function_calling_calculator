from unittest.mock import MagicMock, patch
import groq_api.api as api  # Import the module under test

def test_call_groq_function():
    # Mock the client object and its behavior
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = {
        "choices": [{"message": {"content": "Test response"}}]
    }

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