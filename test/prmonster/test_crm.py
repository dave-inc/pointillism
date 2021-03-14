from pytest import fixture
from os import remove
from prmonster import crm
from prmonster.crm import Connection
from prmonster.crm.models import Repo

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
        assert '"id", "owner", "name"' == fields

    def test_values_from(self, repo):
        fields = crm.values_from(repo)
        assert '1, "angus", "macgyver"' == fields

    def test_insert_select(self, conn, repo):
        conn.insert(repo)
        results = conn.select(Repo)
        results = [result for result in results]
        assert 1 == results[0].id
        # assert results[0].owner == 'angus'
        assert 1 == len(results)
