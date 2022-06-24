import sqlalchemy
from .postgres import metadata
from gul.types import INET, MACADDR

arpentries = sqlalchemy.Table(
    "arpentries",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.BIGINT, primary_key=True),
    sqlalchemy.Column("ip", INET),
    sqlalchemy.Column("mac", MACADDR),
    sqlalchemy.Column("startstamp", sqlalchemy.Time),
    sqlalchemy.Column("stopstamp", sqlalchemy.Time),
    sqlalchemy.Column("device", sqlalchemy.String),
    sqlalchemy.Column("port", sqlalchemy.Integer),
)