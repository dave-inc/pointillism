import logging
from subprocess import CalledProcessError

from .models import Repo, get_dotfiles, find_docs
from .pr.github import *
from .readme import postpend, RemodificationException
from .replaceinplace import replace_dotrefs

POINTILLISM = 'pointillism'


def repos_reader(reposfile):
    """
    Iterates through lines of a .repos file.
    Expects git project format:

    `{owner}/{project}\n`
    """
    with open(reposfile, "r") as repos:
        for line in repos:
            yield Repo.parse(line)


def do_not_update(repo):
    readme_contents = contents(repo, 'README.md')
    if readme_contents is None:
        return False
    return 'pointillism.io' in readme_contents


def devour_repos(*repos, dry_run=False):
    """Run PRMonster on `repos` params."""
    logging.debug("devouring...")
    logging.debug(repos)
    for reposfile in repos:
        logging.info(reposfile)
        for repo in repos_reader(reposfile):
            repo = checkout(repo)  # adding checkout path
            is_updated = False

            # guard clauses
            if do_not_update(repo):
                logging.warn(f"SKIPPING: {str(repo)}. found 'pointillism.io'")
                continue

            try:
                # update files
                dots = get_dotfiles(repo)
                docs = find_docs(repo)
                if docs is None:
                    # TODO repo checkout issue?
                    logging.error(f"No documentation found in {str(repo)}")
                    continue
                logging.info(f"Found {len(docs)} docs.")

                for doc in docs:
                    with open(doc, 'r') as doc_content:
                        content_start = doc_content.read()
                    if POINTILLISM in content_start:
                        logging.info(f"SKIPPING DOC: {doc}. pointillism found.")
                        continue

                    for dot in dots:
                        content = replace_dotrefs(repo, content_start, dot)
                        with open(doc, 'w') as doc_fp:
                            doc_fp.write(content)
                        if POINTILLISM in content:
                            logging.info(f"inline replace: {doc}")
                            is_updated = True

                # don't postpend if updated any file
                if not is_updated and postpend(repo):
                    logging.info(f"postpend update: {doc}")
                    is_updated = True

                if is_updated:
                    # commit changes
                    commit(repo, '"Adding pointillism.io"')

                    if not dry_run:
                        pr(repo)
                    else:
                        logging.info("DRY RUN: Skipping Publish")
            except CalledProcessError as ex:
                logging.exception(ex)
                continue
            except RemodificationException as ex:
                logging.info(f"Skipping: {ex}")
                continue
