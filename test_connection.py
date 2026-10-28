"""Step 4: Test the connection to Supabase and check that the books table exists."""

import sys

from db import TABLE, count_books, get_client


def main():
    try:
        client = get_client()
        rows = count_books(client)
    except Exception as error:
        print(f"Connection FAILED: {error}")
        sys.exit(1)

    print(f"Connection OK — table '{TABLE}' currently has {rows} rows.")


if __name__ == "__main__":
    main()
