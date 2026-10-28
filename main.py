"""Step 5: Scraper + Supabase — scrape books.toscrape.com and store the results."""

from db import count_books, get_client, save_books
from scraper import BASE_URL, scrape_books


def main():
    client = get_client()

    books = scrape_books()
    print(f"Scraped {len(books)} books from {BASE_URL}")

    written = save_books(client, books)
    print(f"Saved {written} books to Supabase")
    print(f"Table now has {count_books(client)} rows")


if __name__ == "__main__":
    main()
