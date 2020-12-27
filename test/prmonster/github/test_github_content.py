from prmonster.github.search import GitHubContent

# TODO make this a non customer URL
TEST_URL = "https://api.github.com/repositories/185259189/contents/docs/README.md?ref=ea0981727708be93dbe04c0c5894204372dd3a96"


class TestGitHubContent:
    def test_fetch_content(self):
        """ integ test, prone to fail """
        client = GitHubContent()
        body = client.fetch(TEST_URL)
        assert 'Welcome' in body

