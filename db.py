"""Supabase helpers: create the client, test the connection, save and read books."""

import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from supabase import Client, create_client

TABLE = "books"


def get_client() -> Client:
    """Create a Supabase client from SUPABASE_URL and SUPABASE_KEY in the .env file."""
    load_dotenv()
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    if not url or not key:
        raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set in .env (see .env.example)")
    return create_client(url, key)


def count_books(client: Client) -> int:
    """Return the number of rows in the books table."""
    response = client.table(TABLE).select("id", count="exact").limit(1).execute()
    return response.count


def save_books(client: Client, books: list) -> int:
    """Insert books, or update them if their product_url already exists. Returns rows written."""
    now = datetime.now(timezone.utc).isoformat()
    rows = [{**book, "scraped_at": now} for book in books]
    response = client.table(TABLE).upsert(rows, on_conflict="product_url").execute()
    return len(response.data)


def fetch_all_books(client: Client, page_size: int = 1000) -> list:
    """Read every row of the books table (Supabase returns max 1000 rows per request)."""
    books = []
    start = 0
    while True:
        response = client.table(TABLE).select("*").order("id").range(start, start + page_size - 1).execute()
        books.extend(response.data)
        if len(response.data) < page_size:
            return books
        start += page_size
