import os
from supabase import create_client, Client
from google import genai
from dotenv import load_dotenv

load_dotenv()

supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY"),
)

gemini_client = genai.Client()