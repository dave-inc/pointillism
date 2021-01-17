from os import environ
from pytest import mark
from prmonster.github.search import GitHubContent

# TODO make this a non customer URL
WITHOUT_TOKEN = environ.get("GIT_TOKEN") is None
TEST_URL = "https://api.github.com/repositories/185259189/contents/docs/README.md?ref=ea0981727708be93dbe04c0c5894204372dd3a96"


# DISABLED INTEG TEST
class IntegGitHubContent:
    @mark.skipif(WITHOUT_TOKEN, reason="Need GIT_TOKEN env to run")
    def test_fetch_content(self):
        """ integ test, prone to fail """
        client = GitHubContent()
        body = client.fetch(TEST_URL)
        assert isinstance(body, str)
        # assert 'Welcome' in body

