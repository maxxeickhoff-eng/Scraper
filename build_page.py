"""Step 6: Build a searchable HTML overview (index.html) of all books stored in Supabase."""

import json
from datetime import datetime
from pathlib import Path

from db import fetch_all_books, get_client

TEMPLATE = Path(__file__).parent / "templates" / "page.html"
OUTPUT = Path(__file__).parent / "index.html"
FIELDS = ["title", "price", "rating", "in_stock", "product_url", "image_url"]


def build_page(client) -> int:
    """Read the books from Supabase and write them into index.html. Returns the number of books."""
    rows = fetch_all_books(client)
    books = [{field: row[field] for field in FIELDS} for row in rows]

    latest = max((row["scraped_at"] for row in rows), default=None)
    updated = datetime.strptime(latest[:10], "%Y-%m-%d").strftime("%d %b %Y") if latest else "never"

    # "</" inside the JSON would end the <script> tag early, so escape it
    books_json = json.dumps(books, ensure_ascii=False).replace("</", "<\\/")

    html = TEMPLATE.read_text(encoding="utf-8")
    html = html.replace("__BOOKS_JSON__", books_json).replace("__UPDATED__", updated)
    OUTPUT.write_text(html, encoding="utf-8")
    return len(books)


if __name__ == "__main__":
    count = build_page(get_client())
    print(f"Built {OUTPUT.name} with {count} books — open it in your browser")
