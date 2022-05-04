import pymongo
from optimade.server.entry_collections.mongo import MongoCollection
from optimade.server.config import CONFIG

CLIENT = pymongo.MongoClient(
    CONFIG.mongo_uri, connectTimeoutMS=5000, serverSelectionTimeoutMS=5000
)


class OdbxMongoCollection(MongoCollection):
    """Wrap the default optimade collection to prevent Mongo errors from
    directly being displayed to user.

    """

    def __init__(self, indexes=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.collection.create_indexes(indexes)

    def find(self, *args):
        try:
            return super().find(*args)
        except (
            pymongo.errors.ServerSelectionTimeoutError,
            pymongo.errors.ConnectionFailure,
        ):
            raise RuntimeError(
                "Backend currently unavailable, please try again in a few minutes.\n"
                f"Report further issues to web@odbx.science."
            )
