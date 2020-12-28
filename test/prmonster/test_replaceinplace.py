from pytest import fixture

from prmonster.replaceinplace import replace_dotrefs
from prmonster.models import Repo

REPLACEMENT_URL = \
    'https://pointillism.io/twitter/nodes/master/src/main/java/com/twitter/nodes_examples/search/graph.dot.png'


class TestReplaceInPlace:
    @fixture
    def repo(self):
        return Repo(owner='twitter',
                    project='nodes',
                    path='test/fixture/')

    @fixture
    def readme_md(self):
        with open("test/fixtures/README_WITH_REF.md") as md:
            return md.read()

    def test_replaceinplace(self, repo, readme_md):
        dot_name = 'graph.dot'
        result = replace_dotrefs(repo, readme_md, dot_name)
        assert REPLACEMENT_URL in result
