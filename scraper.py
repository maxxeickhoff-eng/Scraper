"""Step 1: Scrape all pages of https://books.toscrape.com."""

from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/"

# The site encodes the star rating as a CSS class, e.g. <p class="star-rating Three">
RATING_WORDS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def fetch_page(url: str) -> BeautifulSoup:
    """Download a page and return it as a parsed BeautifulSoup object."""
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    # The site serves UTF-8 but doesn't declare it, so set it explicitly (fixes the "Â£" issue)
    response.encoding = "utf-8"
    return BeautifulSoup(response.text, "html.parser")


def parse_book(article, page_url: str) -> dict:
    """Extract all fields of one book from its <article class="product_pod"> element."""
    link = article.h3.a
    rating_class = article.find("p", class_="star-rating")["class"][1]
    price_text = article.find("p", class_="price_color").get_text(strip=True)

    return {
        "title": link["title"],
        "price": float(price_text.replace("£", "")),
        "currency": "GBP",
        "rating": RATING_WORDS.get(rating_class),
        "in_stock": "In stock" in article.find("p", class_="availability").get_text(),
        "product_url": urljoin(page_url, link["href"]),
        "image_url": urljoin(page_url, article.find("img")["src"]),
    }


def scrape_books(url: str = BASE_URL) -> list:
    """Scrape every book in the catalogue by following the 'next' link across all pages."""
    books = []
    while url:
        soup = fetch_page(url)
        articles = soup.find_all("article", class_="product_pod")
        books.extend(parse_book(article, url) for article in articles)

        next_link = soup.find("li", class_="next")
        url = urljoin(url, next_link.a["href"]) if next_link else None
    return books


if __name__ == "__main__":
    # Step 2: make sure data is flowing — print what we scraped
    books = scrape_books()
    print(f"Scraped {len(books)} books from {BASE_URL}\n")
    for book in books:
        print(f"{book['rating']}★  £{book['price']:>6.2f}  {book['title']}")
