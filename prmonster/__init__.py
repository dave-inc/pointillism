import logging
from subprocess import CalledProcessError

from .models import Repo
from .pr.github import *
from .readme import update_readmes, find_docs


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
    readme_contents = contents(repo, 'README.md')
    if readme_contents is None:
        return False
    return 'pointillism.io' in readme_contents


def devour_repos(*repos, dry_run=False):
    """Run PRMonster on `repos` params.
    """
    logging.debug("devouring...")
    logging.debug(repos)
    for filename in repos:
        logging.info(filename)
        for repo in repos_reader(filename):
            repo = checkout(repo)  # adding checkout path

                # guard clauses
            if do_not_update(repo):
                logging.warn(f"SKIPPING: {str(repo)}. found 'pointillism.io'")
                continue

            try:
                # update files
                docs = find_docs(repo)
                if docs is None:
                    # TODO repo checkout issue?
                    continue
                logging.info(f"Found {len(docs)} docs.")

                if not docs:
                    logging.error(f"No documentation found in {str(repo)}")
                    continue

                update_readmes(repo)

                # commit changes
                commit(repo, '"Adding pointillism.io"')

                if not dry_run:
                    pr(repo)
                else
                    logging.info("DRY RUN: Skipping Publish")
            except CalledProcessError as ex:
                logging.exception(ex)
                continue
