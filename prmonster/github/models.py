from json import loads


class GHRepo:
    def __init__(self, owner, project):
        self.owner = owner
        self.project = project

    def __str__(self):
        return f"Repo\t{self.owner}/{self.project}"


class GHSearchItem:
    def __init__(self, item):
        self.path = item['path']
        self.url = item['url']
        self.repo = item['repository']['full_name']

    def content_url(self):
        return f"https://raw.githubusercontent.com/{self.repo}/master/{self.path}>"

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

