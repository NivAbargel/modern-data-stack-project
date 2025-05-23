# ingestion/api_ingest.py

# import os  # to load env vars
# import requests  # to call the GitHub API
# import psycopg2  # PostgreSQL client library for Python
# from dotenv import load_dotenv  # to load variables from your .env file (like the GitHub token)
#
# # Load environment variables from the .env file
# load_dotenv()
#
# GITHUB_USER = "NivAbargel"
# GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
#
# HEADERS = {
#     "Authorization": f"token {GITHUB_TOKEN}"
# }
#
#
# def get_postgres_connection():
#     """
#     Establishes a connection to the PostgreSQL container
#     using credentials defined in docker-compose.
#
#     Returns:
#         psycopg2.extensions.connection: A live PostgreSQL connection object
#     """
#     return psycopg2.connect(
#         host="postgres",  # Service name from docker-compose
#         dbname="modern_data_stack",
#         user="airflow",
#         password="airflow"
#     )
#
#
# # SQL for table creation
# CREATE_USERS_TABLE = """
# CREATE TABLE IF NOT EXISTS github_users (
#     id BIGINT PRIMARY KEY,
#     login TEXT,
#     name TEXT,
#     location TEXT,
#     public_repos INTEGER,
#     followers INTEGER,
#     created_at TIMESTAMPTZ
# );
# """
#
# CREATE_REPOS_TABLE = """
# CREATE TABLE IF NOT EXISTS github_repos (
#     id BIGINT PRIMARY KEY,
#     name TEXT,
#     full_name TEXT,
#     user_id BIGINT REFERENCES github_users(id),
#     html_url TEXT,
#     description TEXT,
#     language TEXT,
#     stargazers_count INTEGER,
#     forks_count INTEGER,
#     created_at TIMESTAMPTZ,
#     updated_at TIMESTAMPTZ
# );
# """
#
#
# def create_tables(cur):
#     """
#     Executes SQL commands to create github_users and github_repos
#     tables if they don't already exist.
#
#     Args:
#         cur (psycopg2.extensions.cursor): An open database cursor
#     """
#     cur.execute(CREATE_USERS_TABLE)
#     cur.execute(CREATE_REPOS_TABLE)
#
#
# def fetch_user_data(username):
#     """
#     Fetches user metadata from the GitHub API.
#
#     Args:
#         username (str): GitHub username to fetch data for
#
#     Returns:
#         dict: JSON response containing user metadata
#     """
#     url = f"https://api.github.com/users/{username}"
#     response = requests.get(url, headers=HEADERS)
#
#     if response.status_code != 200:
#         raise Exception(f"GitHub API error: {response.status_code} - {response.text}")
#
#     return response.json()
#
#
# def insert_user_data(cur, user_data):
#     """
#     Inserts a GitHub user's metadata into the database.
#
#     Args:
#         cur (psycopg2.extensions.cursor): Active database cursor
#         user_data (dict): Parsed GitHub API user response
#     """
#     cur.execute("""
#         INSERT INTO github_users (id, login, name, location, public_repos, followers, created_at)
#         VALUES (%s, %s, %s, %s, %s, %s, %s)
#         ON CONFLICT (id) DO NOTHING; -- safe to run again, no overwriting ()
#     """, (
#         user_data.get("id"),
#         user_data.get("login"),
#         user_data.get("name"),
#         user_data.get("location"),
#         user_data.get("public_repos"),
#         user_data.get("followers"),
#         user_data.get("created_at")
#     ))
#
#
# if __name__ == "__main__":
#     conn = get_postgres_connection()
#     cur = conn.cursor()
#
#     create_tables(cur)  # ensure tables exist
#
#     user = fetch_user_data(GITHUB_USER)
#     insert_user_data(cur, user)
#
#     conn.commit()
#     cur.close()
#     conn.close()


import os  # to load env vars
import requests  # to call the GitHub API
import psycopg2  # PostgreSQL client library for Python
from dotenv import load_dotenv  # to load variables from your .env file (like the GitHub token)

# Load environment variables from the .env file
load_dotenv()

GITHUB_USERS = ["NivAbargel", "torvalds", "mojombo", "defunkt"]


def get_postgres_connection():
    """
    Establishes a connection to the PostgreSQL container
    using credentials defined in docker-compose.

    Returns:
        psycopg2.extensions.connection: A live PostgreSQL connection object
    """
    return psycopg2.connect(
        host="postgres",  # Service name from docker-compose
        dbname="modern_data_stack",
        user="airflow",
        password="airflow"
    )


# SQL for table creation
CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS github_users (
    id BIGINT PRIMARY KEY,
    login TEXT,
    name TEXT,
    location TEXT,
    public_repos INTEGER,
    followers INTEGER,
    created_at TIMESTAMPTZ
);
"""

CREATE_REPOS_TABLE = """
CREATE TABLE IF NOT EXISTS github_repos (
    id BIGINT PRIMARY KEY,
    name TEXT,
    full_name TEXT,
    user_id BIGINT REFERENCES github_users(id),
    html_url TEXT,
    description TEXT,
    language TEXT,
    stargazers_count INTEGER,
    forks_count INTEGER,
    created_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ
);
"""


def create_tables(cur):
    """
    Executes SQL commands to create github_users and github_repos
    tables if they don't already exist.

    Args:
        cur (psycopg2.extensions.cursor): An open database cursor
    """
    cur.execute("DROP TABLE IF EXISTS github_repos CASCADE;")  # ⚠️ Caution - on’t do this in production unless you're okay losing all existing data in the tables.
    cur.execute("DROP TABLE IF EXISTS github_users CASCADE;")  # This is suitable during early development when schema might change frequently.
    cur.execute(CREATE_USERS_TABLE)
    cur.execute(CREATE_REPOS_TABLE)


def fetch_user_data(username):
    """
    Fetches user metadata from the GitHub API.

    Args:
        username (str): GitHub username to fetch data for

    Returns:
        dict: JSON response containing user metadata
    """
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"GitHub API error: {response.status_code} - {response.text}")

    return response.json()


def fetch_user_repos(username):
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"GitHub API error (repos): {response.status_code} - {response.text}")
    return response.json()


def insert_repo_data(cur, repos, user_id):
    for repo in repos:
        cur.execute("""
            INSERT INTO github_repos (id, name, full_name, user_id, html_url, description,
                                      language, stargazers_count, forks_count, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
        """, (
            repo.get("id"),
            repo.get("name"),
            repo.get("full_name"),
            user_id,
            repo.get("html_url"),
            repo.get("description"),
            repo.get("language"),
            repo.get("stargazers_count"),
            repo.get("forks_count"),
            repo.get("created_at"),
            repo.get("updated_at")
        ))


def insert_user_data(cur, user_data):
    """
    Inserts a GitHub user's metadata into the database.

    Args:
        cur (psycopg2.extensions.cursor): Active database cursor
        user_data (dict): Parsed GitHub API user response
    """
    cur.execute("""
        INSERT INTO github_users (id, login, name, location, public_repos, followers, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING; -- safe to run again, no overwriting ()
    """, (
        user_data.get("id"),
        user_data.get("login"),
        user_data.get("name"),
        user_data.get("location"),
        user_data.get("public_repos"),
        user_data.get("followers"),
        user_data.get("created_at")
    ))


if __name__ == "__main__":
    conn = get_postgres_connection()
    cur = conn.cursor()

    create_tables(cur)  # ensure tables exist

    for username in GITHUB_USERS:
        try:
            user = fetch_user_data(username)
            insert_user_data(cur, user)
            repos = fetch_user_repos(username)
            insert_repo_data(cur, repos, user["id"])
            print(f"✅ Inserted data for {username} and their repos.")
        except Exception as e:
            print(f"❌ Error with {username}: {e}")

    conn.commit()
    cur.close()
    conn.close()
