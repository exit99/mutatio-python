"""
TODO:

    Abstract flask and django stuff seperately.
    Pull all the enviroment variables into one place.
    Make the defaults editable via env vars. (anotherwords wherever
    you see app.config.get("BLAH", "EH") just make eh the default in the app.
"""
import os
import re

from .defaults import dashboard_template
from .exceptions import DuplicateTagError


class TagGenerator():
    def __init__(self, db, app=None):
        self.db = db
        self.app = app

    def create_tags(self, template_dir):
        files = self.load_files(template_dir)
        return self.extract_tags(files, template_dir)

    def load_files(self, template_dir):
        """Return a set of the absolute paths of all html files in the path.

        :param template_dir: The absolute path of the template directory.
        """
        file_paths = set()
        for root, subdirs, files in os.walk(template_dir):
            for f in files:
                if f.endswith('.html'):
                    file_paths.add(os.path.join(root, f))
            for subdir in subdirs:
                print subdir

                # TODO: Remove this.
                if subdir == ".ropeproject":
                    print "Skipping..."
                    continue

                file_paths.union(self.load_files(os.path.join(root, subdir)))
        return file_paths

    def extract_tags(self, files, template_dir):
        """Parse the templates and return a dictionary of tags."""
        tags = {}
        for f in files:
            if f.endswith(
                self.app.config.get("MUTATIO_ADMIN", dashboard_template)
            ):
                continue
            with open(f, 'r') as f:
                f_name = self._format_file_name(f, template_dir)
                f_tags = self.tags_list_from_html(f.read())
                self._valid_tags(tags)
            if f_name in tags:
                raise DuplicateTagError()
            tags[f_name] = f_tags
        return tags

    def tags_list_from_html(self, html):
        """Return a list of tag names in the html."""
        expr = ".*?".join(self.app.config.get("MUTATIO_TEMPLATE_TAGS"))
        matches = re.findall(expr, html)
        return [self._remove_template_tags(m) for m in matches]

    def _valid_tags(self, tags):
        if len(tags) != len(set(tags)):
            raise DuplicateTagError()

    def _format_file_name(self, f, template_dir):
        return f.name[len(template_dir) + 1:]

    def _remove_template_tags(self, match):
        return match[2:-2].strip(' ')
