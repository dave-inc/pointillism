import logging
from argparse import ArgumentParser
from prmonster.crm import (
    all_repos, all_resources, repo_count, CONN
)
from prmonster.crm.models import (
    RESOURCE_SELECT, REPO_SORT, REPOS_TOP
)

parser = ArgumentParser(description="pointillism CRM")
parser.add_argument("--user", default=None,
                    help="")
parser.add_argument("--sql", type=str, dest="sql",
                    help="exec arbitrary SELECT")
args = parser.parse_args()

if args.sql:
    rows = CONN.select(query=args.sql)
    for row in rows:
        print("\t".join(map(str, row)))
    exit(0)

if args.user is None:
    repos = CONN.select(query=REPOS_TOP)
    for repo in repos:
        print("\t".join(map(str, repo)))

    print(f"Repo Count: {repo_count()}")
