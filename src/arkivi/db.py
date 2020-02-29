import enum
from collections import namedtuple
from cached_property import cached_property
from pyArango.connection import Connection


class Collections(enum.Enum):
    SPECTACLES = 'spectacles'


DB_CONFIG = namedtuple('DB', ['user', 'password', 'database'])


class Database:

    def __init__(self, **config):
        self.config = DB_CONFIG(**config)

    @cached_property
    def db(self):
        conn = Connection(
            username=self.config.user,
            password=self.config.password
        )
        name = self.config.database
        if not conn.hasDatabase(name):
            return conn.createDatabase(name)
        return conn[name]

    def get(self, name):
        collection = Collections(name).value
        db = self.db
        if not db.hasCollection(collection):
            return db.createCollection(name=collection)
        return db.collections[collection]

    def __getitem__(self, name):
        collection = Collections(name).value
        return db.collections[collection]

    def __contains__(self, name):
        collection = Collections(name).value
        return self.db.hasCollection(collection)

    def query(self, aql: str, *args, **kwargs):
        return self.db.AQLQuery(aql, *args, **kwargs)
