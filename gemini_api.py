import os

# Try to load a .env file if python-dotenv is installed.
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    # dotenv not available — that's fine, we'll just use environment variables
    pass

from google import genai

# Read API key from environment
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    # Clear, actionable error message for beginners
    raise ValueError(
        "GEMINI_API_KEY is not set. "
        "Set it in your environment or put `GEMINI_API_KEY=your_key` in a .env file.\n"
        "On macOS/Linux: export GEMINI_API_KEY=your_key\n"
        "On Windows (PowerShell): $env:GEMINI_API_KEY='your_key'"
    )

# Create client with the API key
client = genai.Client(api_key=api_key)

def _mask_key(s: str, key: str) -> str:
    # Replace occurrences of the key with a mask to avoid leaking it in logs/errors.
    if not key:
        return s
    return s.replace(key, "****[REDACTED]****")

try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Explain how AI works in a few words"
    )
    # Print only the model text output (don't print full response objects)
    if hasattr(response, "text"):
        print(response.text)
    else:
        print(str(response))
except Exception as e:
    # Print a short, safe error message and mask any occurrence of the API key
    safe_msg = _mask_key(str(e), api_key)
    print("Request failed:", safe_msg)
    # Optionally re-raise if you want a traceback during development:
    # raise
