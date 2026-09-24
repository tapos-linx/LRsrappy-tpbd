import json
import os
from google import genai

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Missing GEMINI_API_KEY environment variable.")

client = genai.Client(api_key=GEMINI_API_KEY)

# 1. Call Gemini with your extraction instruction / scraping input
prompt = """
Extract and structure the latest data into the JSON schema defined in system instructions.
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
    config={
        "response_mime_type": "application/json",
    },
)

# 2. Parse response and write files directly to disk
payload = json.loads(response.text)
for file_entry in payload.get("files", []):
    path = file_entry["path"]
    content = file_entry["content"]

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Updated {path}")
