"""Step 5: Scraper + Supabase — scrape books.toscrape.com, store the results, build the overview page."""

from build_page import OUTPUT, build_page
from db import count_books, get_client, save_books
from scraper import BASE_URL, scrape_books


def main():
    client = get_client()

    books = scrape_books()
    print(f"Scraped {len(books)} books from {BASE_URL}")

    written = save_books(client, books)
    print(f"Saved {written} books to Supabase")
    print(f"Table now has {count_books(client)} rows")

    build_page(client)
    print(f"Updated {OUTPUT.name} — open it in your browser")


if __name__ == "__main__":
    main()
