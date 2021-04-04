import logging
from prmonster.crm import (
    all_repos, all_resources, repo_count, CONN
)
from prmonster.crm.models import RESOURCE_SELECT, REPO_SORT, REPOS_TOP


repos = CONN.select(query=REPOS_TOP)
for repo in repos:
    print("\t".join(map(str, repo)))

print(f"Repo Count: {repo_count()}")
