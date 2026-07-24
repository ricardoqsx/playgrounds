import os

from sqlalchemy import create_engine


def get_int_env(name, default):
    return int(os.environ.get(name, default))


def build_database_url():
    user = os.environ.get("DB_USER", "playgrounds")
    password = os.environ.get("DB_PASSWORD", "playgrounds")
    host = os.environ.get("DB_HOST", "mariadb")
    port = os.environ.get("DB_PORT", "3306")
    database = os.environ.get("DB_NAME", "playgrounds")
    return f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"


engine = create_engine(
    build_database_url(),
    pool_size=get_int_env("DB_POOL_SIZE", 5),
    max_overflow=get_int_env("DB_MAX_OVERFLOW", 10),
    pool_timeout=get_int_env("DB_POOL_TIMEOUT", 30),
    pool_recycle=get_int_env("DB_POOL_RECYCLE", 1800),
    pool_pre_ping=True,
    connect_args={
        "charset": "utf8mb4",
        "autocommit": True,
        "connect_timeout": get_int_env("DB_CONNECT_TIMEOUT", 10),
        "read_timeout": get_int_env("DB_READ_TIMEOUT", 30),
        "write_timeout": get_int_env("DB_WRITE_TIMEOUT", 30),
    },
)


class PooledConnection:
    def __init__(self, conn):
        self.conn = conn

    def __enter__(self):
        return self.conn

    def __exit__(self, exc_type, exc, tb):
        self.conn.close()


def get_conn():
    return PooledConnection(engine.raw_connection())
