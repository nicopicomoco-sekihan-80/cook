import os

from dotenv import load_dotenv
from google import genai


load_dotenv()

api_key = os.environ["GEMINI_API_KEY"]

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="こんにちは。料理アシスタントとして一言だけ返してください。",
)

print(response.text)
