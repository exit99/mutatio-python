from pymongo import MongoClient


def mongo_connection(db, host, port):
    """Return the connection to the mutatio mongo database.

    :param db: The name of the mongo database.
    :param host: The host where the mongo instance is located.
    :param port: The port where the mongo instance is located.

    `host` and `port` default to the host and port used by the
    development Vagrantfile.
    """
    client = MongoClient(host, port)
    db = client[db]
    return db
