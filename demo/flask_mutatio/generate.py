import os
import re

from bs4 import BeautifulSoup


class TagGenerator():
    def create_tags(self, template_dir):
        files = self.load_files(template_dir)
        tags = self.extract_tags(files, template_dir)
        import pdb; pdb.set_trace()

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
        t = {}
        for f in files:
            with open(f, 'r') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
                tags = soup.find_all(mutatio=True)
                f_name = f.name[len(template_dir) + 1:][:-5].replace('/', '_')
            for tag in tags:
                tag_name = tag['mutatio']
                if f_name not in t.keys():
                    t[f_name] = {}
                if tag_name not in t[f_name].keys():
                    t[f_name][tag_name] = set()
                tag_set = self.fetch_template_tags(tag.text)
                t[f_name][tag_name] = t[f_name][tag_name].union(tag_set)
        return t

    def fetch_template_tags(self, text):
        # Make these so you can change somewhere.
        start = '{@'
        end = '@}'
        var = '{}.+?{}'.format(start, end)
        matches = re.findall(var, text)
        return set([m[len(start):-len(end)].strip(' ') for m in matches])
