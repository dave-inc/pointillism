from pytest import fixture
from prmonster.github import GHSearchResponse, GHSearchItem


class TestGithubSearchParse:
    @fixture
    def github_response(self):
        with open("test/fixtures/gh-search.json") as ghs:
            return ghs.read()

    def test_parse(self, github_response):
        resp = GHSearchResponse.from_json(github_response)
        assert resp.total == 7
        for item in resp.items:
            print(item)