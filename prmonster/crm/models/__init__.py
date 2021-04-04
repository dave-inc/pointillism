from os import path, environ

SQL_PATH = environ.get("SQL_PATH",
                       path.dirname(__file__) +\
                       "/../sql/%s.sql")

def load_sql(name):
    return open(SQL_PATH % name, 'r').read()

REPO_COUNT = load_sql('repo_count')
REPO_SORT = load_sql('repos')
REPOS_TOP = load_sql('repos_top')
RESOURCE_SELECT = load_sql("resources")
REPOS_OVER_DAYS = load_sql('repos_over_days')

CREATE_SQL = ["""
CREATE TABLE leads (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email VARCHAR(255),
  name VARCHAR(255),
  owner VARCHAR(255),
  created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated TIMESTAMP
);""",
"""
CREATE TABLE repos (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  lead_id INTEGER,
  owner VARCHAR(255), -- github account
  name VARCHAR(255),  -- project name
  subscribers INTEGER,
  starred INTEGER,
  watchers INTEGER,
  author VARCHAR(255),
  created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated TIMESTAMP,
  UNIQUE(owner, name)
);""",
"""
CREATE TABLE resources (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  repo_id INTEGER,        -- repo which hold this file
  filename VARCHAR(255),
  created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated TIMESTAMP,
  UNIQUE(filename)
);""",
"""
CREATE TABLE refs (
  file_id INTEGER,
  ref_file INTEGER,
  UNIQUE(file_id, ref_file)
);"""
]


class Lead:
    id: int
    email: str
    name: str
    owner: str


class Repo:
    def __init__(self,
                 id=None,
                 _um=None,
                 owner=None,
                 name=None,
                 author=None,
                 subscribers=None,
                 starred=None,
                 watchers=None,
                 *args, **repo_info):
        self.id = id
        self.owner = owner
        self.name = name
        self.author      = author
        self.subscribers = subscribers
        self.starred     = starred
        self.watchers    = watchers

        if repo_info:
            info = repo_info['repo_info']
            self.subscribers = info['subscribers_count']
            self.starred = info['stargazers_count']
            self.watchers = info['watchers_count']

    @property
    def repo_s(self):
        return f"{self.owner}/{self.name}"

    def __repr__(self):
        return f"Repo({self.id}):" + " ".join(map(str, (self.owner,
                                                  self.name)))


class Resource:
    def __init__(self, id=None, repo_id=None, filename=None):
        self.id = id
        self.repo_id = repo_id
        self.filename = filename

    def __repr__(self):
        return f"Resource({self.id}: " + " ".join((
            str(self.repo_id), self.filename
        ))


class Ref:
    file_id: int
    ref_file: int