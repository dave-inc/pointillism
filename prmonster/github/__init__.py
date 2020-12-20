#
# GH file search client
# https://docs.github.com/en/free-pro-team@latest/rest/reference/search
#
from os import environ
from http.client import HTTPSConnection
from base64 import b64encode
from .models import *

USER = "trevorgrayson"
TOKEN = environ['GIT_TOKEN']

userAndPass = b64encode(f"{USER}:{TOKEN}".encode("utf8")).decode("ascii")
HEADERS = {
    'Authorization': 'Basic %s' % userAndPass,
    "accept": "application/vnd.github.v3+json",
    'User-Agent': 'pointillism.io bot'
}
DOMAIN = 'api.github.com'

params = dict(
    q="extension:dot%20extension:gv",
    per_page="100",
    sort="indexed",
    order="desc"
)
URL = '/search/code?' + '&'.join([f"{k}={v}" for k, v in params.items()])


class GitHubFileSearchClient:
    """GitHub File Search Client"""
    def __init__(self):
        self.conn = HTTPSConnection(DOMAIN)

    def url(self, page):
        return URL + f"&page={page}"

    def search(self, page=0):
        print(self.url(page))
        self.conn.request('GET', self.url(page), headers=HEADERS)
        resp = self.conn.getresponse()

        if resp.status == 200:
            return GHSearchResponse.from_json(resp.read())
        else:
            raise Exception(f"{resp.status}: {resp.read()}")
