"""Asks for your Supabase URL and key, writes them to .env and tests the connection."""

from getpass import getpass

from test_connection import main as test_connection


def main():
    print("Paste your Supabase values (see README → Setup).\n")
    url = input("Project URL (https://....supabase.co): ").strip().rstrip("/")
    key = getpass("Secret key (input is hidden): ").strip()

    if not url.startswith("https://") or not key:
        print("URL must start with https:// and the key must not be empty. Please try again.")
        return

    with open(".env", "w") as env_file:
        env_file.write(f"SUPABASE_URL={url}\nSUPABASE_KEY={key}\n")
    print("\nSaved to .env — testing connection...\n")

    test_connection()


if __name__ == "__main__":
    main()
