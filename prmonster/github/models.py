import logging
from json import loads


class GHRepo:
    def __init__(self, owner, project):
        self.owner = owner
        self.project = project
        self.dots = None
        self.refs = None

    def __str__(self):
        return f"Repo\t{self.owner}/{self.project}"

    def report(self):
        """Summary for repo PR consideration"""
        return f"{self.owner}/{self.project}\tdots:{self.dots}\tref:{self.refs}"

class GHSearchItem:
    def __init__(self, item):
        self.path = item['path']
        self.url = item['url']
        self.repo = item['repository']['full_name']

    def content_url(self):
        """
        TODO master may be main, or other branch name
        """
        return f"https://raw.githubusercontent.com/{self.repo}/master/{self.path}"

    def filename(self, ext=False):
        try:
            return self.path.split("/")[-1].split(".")[0]
        except ex:
            logging.error("Couldn't lazy parse: " + self.path)
            return None

    def filetype(self):
        try:
            return self.path.split(".")[-1]
        except ex:
            logging.error("Couldn't lazy format: " + self.path)
            return None

    def __str__(self):
        return f"GHItem\t{self.content_url()}"


class GHSearchResponse:
    def __init__(self, response):
        self.total = response.get("total_count")
        self.incomplete = response.get("incomplete_results")
        self.items = [GHSearchItem(item) for item in response['items']]

    @classmethod
    def from_json(cls, json):
        return GHSearchResponse(loads(json))

    @property
    def count(self):
        return len(self.items)

    def repos(self):
        """return unique repos in results"""
        repos = set([item.repo for item in self.items])
        return list(repos)

    def __str__(self):
        return f"GitHubSearch\t{self.count}/{self.total}\tincomplete={self.incomplete}"

