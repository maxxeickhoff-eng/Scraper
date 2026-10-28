# Books Scraper → Supabase

A small Python web scraper that collects book data from [books.toscrape.com](https://books.toscrape.com) and stores it in a [Supabase](https://supabase.com) (PostgreSQL) table.

## Project structure

| File | Purpose | Assignment step |
|---|---|---|
| `scraper.py` | Scrapes the first page (20 books) with `requests` + `BeautifulSoup` | 1. Build the scraper, 2. Data is flowing |
| `schema.sql` | SQL to create the `books` table in Supabase | 3. Create a matching table |
| `db.py` | Supabase client + helpers (count, upsert) | 4 & 5 |
| `test_connection.py` | Checks that credentials work and the table exists | 4. Test the connection |
| `main.py` | Scrapes and saves the books to Supabase | 5. Merge scraper + Supabase |

## Data model

Each book is scraped into this shape and stored as one row:

| Column | Type | Example |
|---|---|---|
| `id` | bigint (auto) | `1` |
| `title` | text | `A Light in the Attic` |
| `price` | numeric(10,2) | `51.77` |
| `currency` | text | `GBP` |
| `rating` | smallint (1–5) | `3` |
| `in_stock` | boolean | `true` |
| `product_url` | text, unique | `https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html` |
| `image_url` | text | `https://books.toscrape.com/media/cache/2c/da/...jpg` |
| `scraped_at` | timestamptz | `2026-10-28T12:00:00+00:00` |

`product_url` is unique, so running the scraper again **updates** existing rows instead of creating duplicates (upsert).

## Setup

### 1. Install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Create the Supabase project

1. Sign up at [supabase.com](https://supabase.com) and click **New project** (free tier is enough).
2. Open **SQL Editor → New query**, paste the contents of `schema.sql` and click **Run**.
3. Check **Table Editor** — a `books` table should now exist.

### 3. Add your credentials

```bash
cp .env.example .env
```

Fill in `.env`:

- `SUPABASE_URL` — **Project Settings → Data API → Project URL**
- `SUPABASE_KEY` — **Project Settings → API Keys → secret key** (`sb_secret_...`, or the legacy `service_role` key)

The secret key is needed because the table has Row Level Security enabled. Keep it private — `.env` is listed in `.gitignore` and is never pushed to GitHub.

## Usage

```bash
# Step 1 & 2: scrape and print the data (no database needed)
python scraper.py

# Step 4: test the Supabase connection
python test_connection.py

# Step 5: scrape and store in Supabase
python main.py
```

Expected output of `main.py`:

```
Scraped 20 books from https://books.toscrape.com/
Saved 20 books to Supabase
Table now has 20 rows
```

## Notes

- On macOS's built-in Python 3.9 you may see a harmless `NotOpenSSLWarning` from urllib3; it doesn't affect the scraper.
- books.toscrape.com is a sandbox site built for scraping practice, so scraping it is allowed.
