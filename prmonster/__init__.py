import logging
from subprocess import CalledProcessError

from .models import Repo
from .pr.github import *
from .readme import update_readmes


def repos_reader(filename):
    """
    Iterates through lines of a .repos file.
    Expects git project format:

    `{owner}/{project}\n`
    """
    with open(filename, "r") as repos:
        for line in repos:
            yield Repo.parse(line)


def do_not_update(repo):
    return 'pointillism.io' in contents(repo, 'README.md')


def devour_repos(*repos, dry_run=False):
    """Run PRMonster on `repos` params.
    """
    for filename in repos:
        logging.info(filename)
        for repo in repos_reader(filename):
            repo = checkout(repo)  # adding checkout path

            # guard clauses
            if do_not_update(repo):
                logging.info(f"SKIPPING: {str(repo)}. found 'pointillism.io'")
                continue

            try:
                # update files
                update_readmes(repo)

                # commit changes
                commit(repo, '"Adding pointillism.io"')

                if not dry_run:
                    pr(repo)
            except CalledProcessError as ex:
                logging.exception(ex)
                continue
