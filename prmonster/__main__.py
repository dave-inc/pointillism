import logging
from . import *
from .pr.github import *
from .readme import update_readmes
from subprocess import CalledProcessError

from argparse import ArgumentParser

logging.basicConfig(level=logging.INFO)

parser = ArgumentParser()
parser.add_argument("files", type=str, nargs="+",
                    help="files with repos")

class CommitException(Exception): pass

if __name__ == "__main__":
    args = parser.parse_args()

    for filename in args.files:
        logging.info(filename)
        for repo in repos_reader(filename):
            repo = checkout(repo)  # adding checkout path
            if 'pointillism.io' in contents(repo, 'README.md'):
                logging.info(f"SKIPPING: {str(repo)}. found 'pointillism.io'")
                continue

            update_readmes(repo)
            try:
                commit(repo, '"Adding pointillism.io"')
            except CalledProcessError:
                logging.error(
                    f"Commit failure. Does {str(repo)} have DOT files?")
                continue
            try:
                pr(repo)
            except CalledProcessError:
                logging.error(
                    f"PR failure for: {str(repo)}")
