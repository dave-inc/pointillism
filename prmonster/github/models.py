import logging
from json import loads
from datetime import datetime

class GHRepo:
    def __init__(self, owner, project):
        self.owner = owner
        self.project = project
        self.dots = None
        self.refs = None
        self.subscribers_count = 0
        self.stargazers_count = 0
        self.watchers_count = 0

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
    def __init__(self, response, resume=0):
        self.total = response.get("total_count")
        self.incomplete = response.get("incomplete_results")
        self.items = [GHSearchItem(item) for item in response.get('items')]
        self.resume = int(resume)

    @classmethod
    def from_json(cls, json, resume=0):
        return GHSearchResponse(loads(json), resume=resume)

    @property
    def count(self):
        return len(self.items)

    def repos(self):
        """return unique repos in results"""
        repos = set([item.repo for item in self.items])
        return list(repos)

    @property
    def wait(self):
        """ returns true if should wait """
        return self.resume > int(datetime.utcnow().timestamp())

    def __str__(self):
        return f"GitHubSearch\t{self.count}/{self.total}\tincomplete={self.incomplete}"


class RepoReport:
    def __init__(self, repo, dots, dot_refs, author, repo_info):
        self.repo = repo
        self.dots = dots
        self.dot_refs = dot_refs
        self.author = author
        self.repo_info = repo_info

    @property
    def followers(self):
        info = self.repo_info
        return ":".join(map(str, (
            info['subscribers_count'],
            info['stargazers_count'],
            info['watchers_count']
        )))

    def save(self):
        report = open(REPORT_PATH, 'w')
        report.write(datetime.strftime(datetime.now(),
                                       "# Report: %Y-%m-%d\n\n"))
        report.write("## Repos\n\n")
        report.write("| repo | dots | refs | author | link |\n")
        report.write("| ---- | ---- | ---- | ------ | ---- |\n")

        for report in self.reports:
            report.write(f"| {repo.owner}/{repo.name} | {len(dots)} | {len(dot_refs.items)} | {author}| [link](https://github.com/{repo}) |\n")

        report.write("Repo Count: %s\n", str(repo_count))
        report.close()

    def __str__(self):
        return f"{self.followers}"
