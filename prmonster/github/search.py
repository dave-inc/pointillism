import logging
import json
from time import sleep
from datetime import datetime
from os import environ
from http.client import HTTPSConnection
from base64 import b64encode, b64decode
from .models import *

USER = "trevorgrayson"
TOKEN = environ.get('GIT_TOKEN')

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
LAST_COMMIT = 'https://api.github.com/repos/%s/commits'
REPO_INFO = 'https://api.github.com/repos/%s'

USER_DOT_FILE_SEARCH = "user%3Agithub+user%3Aatom+user%3Aelectron+user%3Aoctokit+user%3Atwitter+extension%3Adot+extension%3Agv&type=code"
DOT_FILE_SEARCH = "l=&o=desc&q=extension%3Adot+extension%3Agv&s=indexed&type=Code"
# OR *.svg files


class EnhanceCalm(Exception):
    pass


class ClientException(Exception):
    pass


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

    def repo_info(self, repo_s):
        url = REPO_INFO % (repo_s)
        self.conn.request('GET', url, headers=HEADERS)
        resp = self.conn.getresponse()
        if resp.status == 200:
            return json.loads(resp.read())
            # repo.subscribers_count = data['watchers_count']
            # repo.stargazers_count = data['watchers_count']
            # repo.watchers_count = data['watchers_count']

    def last_author(self, repo):
        """
        :param repo: in format of {owner}/{project}
        :return:
        """
        url = LAST_COMMIT % (repo)
        self.conn.request('GET', url, headers=HEADERS)
        resp = self.conn.getresponse()
        if resp.status == 200:
            author = json.loads(resp.read())[0]['commit']['author']
            return author


class GitHubFileSearchClient:
    """GitHub File Search Client"""
    def __init__(self):
        self.conn = HTTPSConnection(DOMAIN)
        self.resume = None

    def url(self, query, page, params):
        # TODO confirm + over %20
        qparams = '+'.join([f"{k}:{v}" for k, v in params.items()])
        suffix = "&q=" + qparams + "+" + query + f"&page={page}"
        return URL + suffix

    def search(self, query=DOT_FILE_SEARCH, page=0, **params):
        url = self.url(query, page, params)
        logging.info(f"SEARCHING\thttps://{DOMAIN}{url}\t{str(params)}")
        self.conn.request('GET', url, headers=HEADERS)
        resp = self.conn.getresponse()

        limit = resp.getheader('X-RateLimit-Limit')
        remaining = resp.getheader('X-RateLimit-Remaining')
        self.resume = resp.getheader('X-RateLimit-Reset')
        logging.info(f"Rate Limit: {remaining}/{limit}. Resume: {self.resume}")
        if resp.status == 200:
            return GHSearchResponse.from_json(resp.read(), resume=self.resume)
        elif resp.status == 403:
            raise EnhanceCalm(resp.read())
        else:
            raise ClientException(f"{resp.status}: {resp.read()}")

