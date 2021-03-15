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
  dot_count INTEGER,
  ref_count INTEGER
);""",
"""
CREATE TABLE resources (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  repo_id INTEGER,        -- repo which hold this file
  filename VARCHAR(255)
);""",
"""
CREATE TABLE refs (
  file_id INTEGER,
  ref_file INTEGER
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
                 *args):
        self.id = id
        self.owner = owner
        self.name = name

    def __repr__(self):
        return f"Repo({self.id}):" + " ".join((self.owner,
                                               self.name))


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