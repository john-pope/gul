import sqlalchemy

from gul.types import CIDR, INET, MACADDR

from .postgres import metadata

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

addresses = sqlalchemy.Table(
    "addresses",
    metadata,
    sqlalchemy.Column("address", INET, primary_key=True),
    sqlalchemy.Column("mac", MACADDR),
    sqlalchemy.Column("pool", sqlalchemy.Integer),
    sqlalchemy.Column("reserved", sqlalchemy.Boolean),
    sqlalchemy.Column("network", CIDR),
    sqlalchemy.Column("changed", sqlalchemy.Time),
    sqlalchemy.Column("changed_by", sqlalchemy.Integer),
)

leases_history = sqlalchemy.Table(
    "leases_history",
    metadata,
    sqlalchemy.Column("address", INET),
    sqlalchemy.Column("mac", MACADDR),
    sqlalchemy.Column("abandoned", sqlalchemy.Boolean),
    sqlalchemy.Column("starts", sqlalchemy.Time),
    sqlalchemy.Column("ends", sqlalchemy.Time),
)

deviceport = sqlalchemy.Table(
    "deviceport",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("device", sqlalchemy.String),
    sqlalchemy.Column("port", sqlalchemy.Integer),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("description", sqlalchemy.String),
    sqlalchemy.Column("isuplink", sqlalchemy.Integer),
    sqlalchemy.Column("services", sqlalchemy.Integer),
    sqlalchemy.Column("mac", MACADDR),
    sqlalchemy.Column("building", sqlalchemy.String),
    sqlalchemy.Column("building_no", sqlalchemy.Integer),
    sqlalchemy.Column("floor", sqlalchemy.Integer),
    sqlalchemy.Column("room", sqlalchemy.String),
    sqlalchemy.Column("jack", sqlalchemy.String),
    sqlalchemy.Column("laststamp", sqlalchemy.Time),
)
