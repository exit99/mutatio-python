import os
import re

from bs4 import BeautifulSoup


class TagGenerator():
    def __init__(self, db, app=None):
        self.db = db
        self.app = app

    def create_tags(self, template_dir):
        files = self.load_files(template_dir)
        return self.extract_tags(files, template_dir)

    def commit_to_mongo(self, tags):
        """Tag the tag dict and create the intial json documents."""

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
                file_paths.union(self.load_files(os.path.join(root, subdir)))
        return file_paths

    def extract_tags(self, files, template_dir):
        """Parse the templates and return a dictionary of tags."""
        t = set()
        for f in files:
            with open(f, 'r') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
                tags = soup.find_all(mutatio=True)
                f_name = self._format_file_name(f, template_dir)
            for tag in tags:
                tag_name = tag[self.app.config.get('MUTATIO_TAG', 'mutatio')]
                tags = self.fetch_template_tags(tag.text)
                tag_set = map(lambda t: "_".join([f_name, tag_name, t]), tags)
                t.update(tag_set)
        return t

    def fetch_template_tags(self, text):
        start, end = self.app.config.get('MUTATIO_TEMPLATE_TAGS', ('{@', '@}'))
        var = '{}.+?{}'.format(start, end)
        matches = re.findall(var, text)
        return set([m[len(start):-len(end)].strip(' ') for m in matches])

    def _format_file_name(self, f, template_dir):
        return f.name[
            len(template_dir) + 1:
        ].replace('/', '_').replace('.', '_')
