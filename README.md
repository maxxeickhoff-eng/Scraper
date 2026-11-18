# Books Scraper → Supabase

A small Python web scraper that collects book data from [books.toscrape.com](https://books.toscrape.com) and stores it in a [Supabase](https://supabase.com) (PostgreSQL) table.

## Project structure

| File | Purpose | Assignment step |
|---|---|---|
| `scraper.py` | Scrapes the full catalogue (1000 books, 50 pages) with `requests` + `BeautifulSoup` | 1. Build the scraper, 2. Data is flowing |
| `schema.sql` | SQL to create the `books` table in Supabase | 3. Create a matching table |
| `db.py` | Supabase client + helpers (count, upsert) | 4 & 5 |
| `setup_supabase.py` | Asks for URL + key, writes `.env`, tests the connection | Setup |
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

### 2. Create the table in Supabase

You need a Supabase account and project ([supabase.com](https://supabase.com) → **New project**, free tier is enough).

1. Copy the SQL to your clipboard: `pbcopy < schema.sql` (macOS), or open `schema.sql` and copy everything.
2. In the Supabase dashboard, open your project and click **SQL Editor** in the left sidebar.
3. Paste the SQL and click **Run** (bottom right). You should see *"Success. No rows returned"*.
4. Click **Table Editor** in the left sidebar — the `books` table is now there (still empty).

### 3. Connect the script to Supabase

Get two values from the dashboard (keep the tab open):

- **Project URL** — **Project Settings** (gear icon, bottom left) → **Data API** → *Project URL*
- **Secret key** — **Project Settings** → **API Keys** → *Secret keys* → copy the key starting with `sb_secret_`
  (on older projects: **Legacy API Keys** → `service_role`)

Then run:

```bash
python setup_supabase.py
```

Paste the URL, then the key (the key stays hidden while you paste — that's normal). The script saves both to `.env` and tests the connection right away. You should see:

```
Connection OK — table 'books' currently has 0 rows.
```

Why the secret key? The table has Row Level Security enabled, and the secret key is allowed to write to it. Keep it private — `.env` is in `.gitignore` and is never pushed to GitHub. (You can also create `.env` by hand from `.env.example`.)

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
Scraped 1000 books from https://books.toscrape.com/
Saved 1000 books to Supabase
Table now has 1000 rows
```

## Notes

- On macOS's built-in Python 3.9 you may see a harmless `NotOpenSSLWarning` from urllib3; it doesn't affect the scraper.
- books.toscrape.com is a sandbox site built for scraping practice, so scraping it is allowed.
