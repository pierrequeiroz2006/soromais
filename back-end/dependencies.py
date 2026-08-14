import os
import logging

from supabase import create_client, Client
from google import genai
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("soromais")

# IMPORTANT: this must be the Supabase ANON key, never the service_role key.
# Access control must be enforced by Row Level Security (RLS) policies in the
# Supabase dashboard, not by key secrecy. See supabase/migrations/0001_rls.sql.
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY") or os.getenv("SUPABASE_KEY")
if not SUPABASE_KEY:
    logger.warning("SUPABASE_ANON_KEY / SUPABASE_KEY not set")
if "service_role" in (SUPABASE_KEY or ""):
    logger.error(
        "SUPABASE key looks like a service_role key — swap to the anon key and "
        "enforce access via RLS. A leaked service_role key bypasses all policies."
    )

supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    SUPABASE_KEY,
)

gemini_client = genai.Client()
