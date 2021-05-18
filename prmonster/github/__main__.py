"""
Search github for leads.
"""
from os import environ
import logging
from . import find_dot_repos, repo_describe
import telemetry
from argparse import ArgumentParser

telemetry.add_handler(telemetry.clients.SlackTelemeter(token=None))
logging.basicConfig(level=logging.DEBUG,
                    filename="logs/github_search.log",
                    format="%(asctime)s:%(levelname)s:%(message)s"
                    )
logging.getLogger().addHandler(logging.StreamHandler())

parser = ArgumentParser(description="github PR search")
parser.add_argument("--repo", type=str, dest="repo",
                    help="single repo to lookup, preferred")
parser.add_argument("--user", default=environ.get("TARGET_USER"),
                    help="needed for github search")

args = parser.parse_args()

if args.repo:
    report = repo_describe(args.repo)
    print("=== report ===")
    print(report)
    print(report.dots)
    for ref in report.dot_refs.items:
        print(ref.path)
        print(ref.url)
        # retrieve contents,
        # parse json,
        # render data["_links"]["html"]
        print()
else:
    # NOTE: No TARGET_USER searches for most recent.
    find_dot_repos(environ.get("TARGET_USER"))
