import os


def _env(name, default=""):
    value = os.environ.get(name)
    return value if value is not None and value != "" else default


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    _db_user = _env("MYSQL_USER", "pyuser")
    _db_pass = _env("MYSQL_PASSWORD", "pypass")
    _db_host = _env("MYSQL_HOST", "playdb")
    _db_name = _env("MYSQL_DATABASE", "playdb")

    SQLALCHEMY_DATABASE_URI = _env(
        "DATABASE_URL",
        f"mysql+pymysql://{_db_user}:{_db_pass}@{_db_host}:3306/{_db_name}?charset=utf8mb4",
    )
