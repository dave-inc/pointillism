

class GitResource:
    def __init__(self, owner=None, project=None, branch=None, path=None):
        self.owner = owner
        self.project = project
        self.branch = branch
        self.path = path

    @classmethod
    def parse(cls, url):
        protocol, _, domain, owner, project, *rest = url.split("/")
        return GitResource(
            owner, project, None, "/".join(rest)
        )

    def should_raw(self):
        return self.branch is None or len(self.branch) < 40

    @property
    def analytics_path(self):
        """ value to be reported to ga """
        return "/" + "/".join((
           self.owner, self.project, self.branch, self.path
        ))

    @property
    def pointillism_path(self):
        if self.should_raw():
            url = [self.owner, self.project]
            if self.branch:
                url.append(self.branch)
            url.append(self.path)
            return "/" + "/".join(url)
        else:
            return f'/{self.owner}/{self.project}/blob/{self.branch}/{self.path}'

    def __str__(self):
        return 'https://github.com' + self.pointillism_path
