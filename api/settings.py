import os
from dataclasses import dataclass
from typing import Literal
from databases import DatabaseURL

from dotenv import load_dotenv
import ssl

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
    verify_certificate: bool
    ssl_object: ssl.SSLContext | bool = None

    def __post_init__(self):
        if self.ssl:
            self.ssl_object = True

            if not self.verify_certificate:
                self.ssl_object = ssl.create_default_context()
                self.ssl_object.check_hostname = False
                self.ssl_object.verify_mode = ssl.CERT_NONE

    def __str__(self):
        port = ':'+self.port if self.port else ''
        ssl_param = ''

        if self.ssl:
            ssl_param = 'ssl=true'

        return (
            f"{self.scheme}://{self.username}:{self.password}@{self.hostname}{port}/{self.database}?{ssl_param}"
        )

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
    ssl=os.environ.get("DB_USE_SSL", 'true') == 'true',
    verify_certificate=os.environ.get("DB_VERIFY_CERTIFICATE") == 'true'
)

# load from env
db_url = DatabaseURL(str(db_config))
