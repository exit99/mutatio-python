from .connection import mongo_connection
from .defaults import dashboard_template, sep
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
            app.config.get("MUTATIO_PORT", 27017)
        )
        self.app = app
        self.tags = self.gen_tags()
        self.commit_tags(self.tags)
        FlaskDashboard(self.db, self.tags, self.app)
        return app

    def gen_tags(self):
        """Return dictionary of tags generated for each template directory.

        :param app: The current Flask application.
        """
        tags = {}
        self.tag_generator = TagGenerator(self.db, self.app)
        for path in self.app.jinja_loader.searchpath:
            p_tags = self.tag_generator.create_tags(path)
            self._valid_tags(tags, p_tags)
            tags.update(p_tags)
        return tags

    def commit_tags(self, tags):
        """Get or create documents for each tag in mongo.

        :param tags: Dictionary of tags from the current app.

        The name of the individual tag  will be the
        collection names in mongo. The actual stored document is the
        content stored for display.
        """
        import pdb; pdb.set_trace()
        assert 0, "YOU ARE HERE. SAVING THE TAGS TO MONGO IN THE CORRECT FORMAT"
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

    def _valid_tags(self, tags, p_tags):
        for k in p_tags:
            if k in tags:
                raise DuplicateTagError()


class BaseDashboard(object):
    def __init__(self, db, tags):
        self.db = db
        self.tags = tags

    def format_tags_for_view(self, tags):
        """Return nested dictionary of tags."""
        tags = {}
        for full_tag in sorted(self.tags):
            f, tag, name = full_tag.split(sep)
            if f not in tags.keys():
                tags[f] = {}
            if tag not in tags[f].keys():
                tags[f][tag] = {}
            if name not in tags[f][tag].keys():
                tags[f][tag] = {}
            tags[f][tag][name] = self.db[full_tag]
        return tags


class FlaskDashboard(BaseDashboard):
    """Create the mutatio dashboard in flask."""
    def __init__(self, db, tags, app):
        import pdb; pdb.set_trace()
        super(FlaskDashboard, self).__init__(db, tags)
        self.create_flask_dashboard(app)

    def create_flask_dashboard(self, app):
        """Create a dashboard view for flask."""
        from flask import render_template

        @app.route('/admin/mutatio')
        def index():
            template = app.config.get('MUTATIO_ADMIN', dashboard_template)
            tags = self.format_tags_for_view(self.tags)
            return render_template(template, tags=tags)
