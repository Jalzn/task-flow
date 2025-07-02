import os

DB_URL_ENV = "TODO_CLI_DB_URL"

def get_db_url() -> str:
    return os.environ.get(DB_URL_ENV, "sqlite:///database.db")

def set_db_url(url: str):
    os.environ[DB_URL_ENV] = url
