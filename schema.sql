-- Step 3: Table for the scraped books.
-- Run this once in the Supabase dashboard: SQL Editor -> New query -> paste -> Run.

create table if not exists public.books (
    id          bigint generated always as identity primary key,
    title       text           not null,
    price       numeric(10, 2) not null,
    currency    text           not null default 'GBP',
    rating      smallint       check (rating between 1 and 5),
    in_stock    boolean        not null,
    product_url text           not null unique,  -- unique, so re-running the scraper updates instead of duplicating
    image_url   text,
    scraped_at  timestamptz    not null default now()
);

-- Row Level Security: nobody can read/write via the public API by default.
-- The scraper uses the secret key (server-side), which bypasses RLS.
alter table public.books enable row level security;
