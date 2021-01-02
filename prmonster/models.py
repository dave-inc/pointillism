from os import path
from glob import glob


class Repo:
    def __init__(self, owner, project, path=None):
        self.owner = owner
        self.project = project
        self.path = path

    @classmethod
    def parse(cls, s):
        return Repo(*s.strip().split("/"))

    @property
    def repo(self):
        return "/".join((self.owner, self.project))

    def mkpath(self, filename):
        return path.join(self.path, filename)

    def __str__(self):
        return f"Repo<{self.owner}/{self.project}>"


def get_dotfiles(repo: Repo):
    path_len = len(repo.path) + 1  # plus slash
    return [fqn[path_len:] for fqn in glob(path.join(repo.path, "*.dot")) + \
           glob(path.join(repo.path, "*.gv")) + \
           glob(path.join(repo.path, "**/*.dot"), recursive=True) + \
           glob(path.join(repo.path, "**/*.gv"), recursive=True)]



def find_docs(repo: Repo):
    if repo.path is None:
        return None
    return glob(path.join(repo.path, "*.md"), recursive=True) + \
           glob(path.join(repo.path, "*.rst"), recursive=True)
