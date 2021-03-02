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
    def __init__(self, id=None, owner=None):
        self.id = id
        self.owner = owner

    lead_id: int
    name: str
    dot_count: int
    ref_count: int

class Resource:
    id: int
    repo_id: int
    filename: str

class Ref:
    file_id: int
    ref_file: int