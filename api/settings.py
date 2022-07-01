import os
from dataclasses import dataclass
from typing import Union

from databases import DatabaseURL
from dotenv import load_dotenv

load_dotenv()


@dataclass
class DBConfig:
    scheme: str
    username: str
    password: str
    hostname: str
    port: int
    database: str
    ssl: bool
    min_connections: int
    max_connections: int
    verify_certificate: bool
    ssl_object: Union[bool, str] = None

    def __post_init__(self):
        if self.ssl:
            self.ssl_object = True

            if not self.verify_certificate:
                self.ssl_object = "require"

    def __str__(self):
        port = ":" + self.port if self.port else ""
        ssl_param = ""

        if self.ssl:
            ssl_param = "ssl=true"

        return f"{self.scheme}://{self.username}:{self.password}@{self.hostname}{port}/{self.database}?{ssl_param}"

    @property
    def url(self):
        return DatabaseURL(str(self))


db_config = DBConfig(
    scheme=os.environ.get("DB_SCHEME", "postgres+asyncpg"),
    username=os.environ.get("DB_USERNAME"),
    password=os.environ.get("DB_PASSWORD"),
    hostname=os.environ.get("DB_HOSTNAME"),
    port=os.environ.get("DB_PORT"),
    database=os.environ.get("DB_DATABASE"),
    ssl=os.environ.get("DB_USE_SSL", "true") == "true",
    min_connections=int(os.environ.get("DB_MIN_CONNECTIONS", "2")),
    max_connections=int(os.environ.get("DB_MAX_CONNECTIONS", "5")),
    verify_certificate=os.environ.get("DB_VERIFY_CERTIFICATE") == "true",
)

# load from env
db_url = DatabaseURL(str(db_config))
