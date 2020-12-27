import logging
import json
from os import environ
from http.client import HTTPSConnection
from base64 import b64encode, b64decode
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

DEFAULT_PARAMS = dict(
    # generate q in UI and paste here
    # q="extension:dot%20extension:gv",
    per_page="100",
    sort="indexed",
    order="desc"
)
URL = '/search/code?' + '&'.join([f"{k}={v}" for k, v in DEFAULT_PARAMS.items()])
URL2 = '/search?' + '&'.join([f"{k}={v}" for k, v in DEFAULT_PARAMS.items()])

USER_DOT_FILE_SEARCH = "user%3Agithub+user%3Aatom+user%3Aelectron+user%3Aoctokit+user%3Atwitter+extension%3Adot+extension%3Agv&type=code"
DOT_FILE_SEARCH = "extension%3Adot+extension%3Agv&type=code"
# OR *.svg files


class GitHubContent:
    """
    Get contents of a github url.
    May not be used presently.
    """
    def __init__(self):
        self.conn = HTTPSConnection(DOMAIN)

    def fetch(self, url):
        self.conn.request('GET', url, headers=HEADERS)
        resp = self.conn.getresponse()
        if resp.status == 200:
            return b64decode(json.loads(resp.read())['content'])\
                .decode("utf8")


class GitHubFileSearchClient:
    """GitHub File Search Client"""
    def __init__(self):
        self.conn = HTTPSConnection(DOMAIN)

    def url(self, query, page, params):
        # TODO confirm + over %20
        qparams = '+'.join([f"{k}:{v}" for k, v in params.items()])
        suffix = "&q=" + qparams + "+" + query + f"&page={page}"
        return URL + suffix

    def search(self, query=DOT_FILE_SEARCH, page=0, **params):
        logging.info(f"SEARCHING\t{query}\t{str(params)}")
        self.conn.request('GET',
                          self.url(query, page, params),
                          headers=HEADERS)
        resp = self.conn.getresponse()

        if resp.status == 200:
            return GHSearchResponse.from_json(resp.read())
        else:
            raise Exception(f"{resp.status}: {resp.read()}")
