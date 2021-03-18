REPO_SORT = """
SELECT *
FROM repos rep
ORDER BY 
    subscribers DESC,
    starred DESC,
    watchers DESC
"""

RESOURCE_SELECT = """
SELECT 
    res.filename,
    rep.owner,
    rep.name
FROM resources res
JOIN repos rep ON rep.id = res.repo_id
"""

CREATE_SQL = ["""
CREATE TABLE leads (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email VARCHAR(255),
  name VARCHAR(255),
  owner VARCHAR(255)
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
  UNIQUE(owner, name)
);""",
"""
CREATE TABLE resources (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  repo_id INTEGER,        -- repo which hold this file
  filename VARCHAR(255),
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