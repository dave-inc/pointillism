import logging
from argparse import ArgumentParser

from . import devour_repos

DESCRIPTION = """
Read list of repo names `owner/project` from 
a file, and attempt to update their documentation
with pointillism.io links.

- Will postpend pointillism IMG to README.md
"""

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s:%(levelname)s:%(message)s")

parser = ArgumentParser(description=DESCRIPTION)
parser.add_argument("files", type=str, nargs="+",
                    help=".repos files with repos"
                         "on separate lines")
parser.add_argument("dry_run", type=str, nargs="?",
                    help="`1` to withold publishing")

args = parser.parse_args()
dry_run = args.dry_run.lower() in ['1', 'true', 'yes']
if not dry_run:
    logging.warn("Publishing Repo changes.")

devour_repos(*args.files, args.dry_run)
