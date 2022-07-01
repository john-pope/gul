import databases
import sqlalchemy
from settings import db_config, db_url

database = databases.Database(
    db_url,
    ssl=db_config.ssl_object,
    min_size=db_config.min_connections,
    max_size=db_config.max_connections,
)

metadata = sqlalchemy.MetaData()
