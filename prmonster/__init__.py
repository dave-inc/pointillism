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

    def __str__(self):
        return f"Repo<{self.owner}/{self.project}>"

def repos_reader(filename):
    """
    Iterates through line of a repos file.

    Expects git project format:

    {owner}/{project}\n
    """
    with open(filename, "r") as repos:
        for line in repos:
            yield Repo.parse(line)
