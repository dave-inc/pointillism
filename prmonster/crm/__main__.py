from prmonster.crm import all_repos, all_resources, CONN
from prmonster.crm.models import RESOURCE_SELECT

for repo in all_repos():
    print(repo)

CONN.select(query=RESOURCE_SELECT)