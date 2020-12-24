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
    # generate q in UI and paste here
    # q="extension:dot%20extension:gv",
    per_page="100",
    sort="indexed",
    order="desc"
)
URL = '/search/code?' + '&'.join([f"{k}={v}" for k, v in params.items()])
URL2 = '/search?' + '&'.join([f"{k}={v}" for k, v in params.items()])

DOT_FILE_SEARCH = "user%3Agithub+user%3Aatom+user%3Aelectron+user%3Aoctokit+user%3Atwitter+extension%3Adot+extension%3Agv&type=code"
SEARCH_REPO = "repo:{repo} *.png"
# OR *.svg files


class GitHubFileSearchClient:
    """GitHub File Search Client"""
    def __init__(self):
        self.conn = HTTPSConnection(DOMAIN)

    def url(self, query, page):
        suffix = "&q=" + query + f"&page={page}"
        return URL + suffix

    def search(self, query=DOT_FILE_SEARCH, page=0):
        print(self.url(query, page))
        self.conn.request('GET', self.url(query, page), headers=HEADERS)
        resp = self.conn.getresponse()

        if resp.status == 200:
            return GHSearchResponse.from_json(resp.read())
        else:
            raise Exception(f"{resp.status}: {resp.read()}")
