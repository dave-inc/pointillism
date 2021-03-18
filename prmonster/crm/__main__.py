import logging
from prmonster.crm import all_repos, all_resources, CONN
from prmonster.crm.models import RESOURCE_SELECT, REPO_SORT


repos = CONN.select(query=REPO_SORT)
for repo in repos:
    print("\t".join(map(str, repo)))
