from .connection import mongo_connection
from .environment import MutatioEnvironment
from .generate import TagGenerator


class Mutatio():
    """
    **IMPORTANT**
    Do not use multiple templates with the same name, tags will be
    overwritten.
    """
    def init_app(self, app):
        """Initialize Mutatio with a Flask app.

        :param app: The current Flask application.

        The following are taken from the app config:

            The name of the mongo database.
            The host where the mongo instance is located.
            The port where the mongo instance is located.

            `host` and `port` default to the host and port used by the
            development Vagrantfile.
        """
        self.db = mongo_connection(
            app.config.get("MUTATIO_DB", 'mutatio'),
            app.config.get("MUTATIO_HOST", 'localhost'),
            app.config.get("MUTATIO_PORT", 27018)
        )
        self.app = app
        self.tags = self.gen_tags()
        self.commit_tags(self.tags)

    def gen_tags(self):
        """Return dictionary of tags generated for each template directory.

        :param app: The current Flask application.
        """
        tags = set()
        self.tag_generator = TagGenerator(self.db, self.app)
        for path in self.app.jinja_loader.searchpath:
            tags.update(self.tag_generator.create_tags(path))
        return tags

    def commit_tags(self, tags):
        """Get or create documents for each tag in mongo.

        :param tags: Dictionary of tags from the current app.

        The name of the individual tag  will be the
        collection names in mongo. The actual stored document is the
        content stored for display.
        """
        c_names = self.db.collection_names()
        for tag in tags:
            if tag in c_names:
                continue
            c = self.db[tag]
            c.insert_one({'data': None})

    def drop_unused_tags(self):
        """Drop unused tags from the mongo database."""
        tags = self.gen_tags()
        tags.add('system.indexes')
        unused = set(self.db.collection_name()) - tags
        for tag in unused:
            print "Dropping: {}".format(tag)
            self.db.drop_collection(tag)
