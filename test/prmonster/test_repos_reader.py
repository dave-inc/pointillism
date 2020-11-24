from prmonster import repos_reader


class TestReposReader:
    def test_repos_reader(self):
        reader = repos_reader("test/fixtures/tg.repos")
        first = next(reader)

        assert first.owner == "trevorgrayson"
        assert first.project == "pointillism"
