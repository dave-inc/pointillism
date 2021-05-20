from pytest import fixture, mark
from os import remove
from prmonster import crm
from prmonster.crm import Connection, save_report, all_repos, all_resources
from prmonster.crm.models import Repo
from prmonster.github.models import RepoReport

DB_FILE = 'test/fixtures/test.db'

class TestCRM:
    @fixture
    def repo(self):
        return Repo(id=1, owner='angus', name="macgyver")

    @fixture
    def conn(self):
        yield Connection(DB_FILE)
        remove(DB_FILE)

    def test_table_from_class(self, repo):
        table = crm.table_from(repo)
        assert 'repos' == table

    def test_fields_from_class(self, repo):
        fields = crm.fields_from(repo)
        assert fields.startswith('"id", "owner", "name"')

    def test_values_from(self, repo):
        fields = crm.values_from(repo)
        assert fields.startswith('1, "angus", "macgyver"')

    def test_insert_select(self, conn, repo):
        conn.insert(repo)
        results = conn.select(Repo)
        results = [result for result in results]
        assert 1 == results[0].id
        # assert results[0].owner == 'angus'
        assert 1 == len(results)

    @mark.skip("broken")
    def test_save_report(self, repo):
        dots = []
        dot_refs = []
        author = 'bob'
        repo_info = None
        report = RepoReport('angus/macgyver', dots, dot_refs, author, repo_info)
        save_report(report)

        repos = all_repos()
        # assert 1 == len([repo for repo in repos])
