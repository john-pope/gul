import databases
import sqlalchemy
from sqlalchemy.dialects import postgresql

from settings import db_url, db_config
database = databases.Database(db_url, ssl=db_config.ssl_object)

metadata = sqlalchemy.MetaData()



