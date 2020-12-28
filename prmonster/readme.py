import logging
from os import path
from glob import glob
from prmonster import Repo
from prmonster.models import get_dotfiles

POINTILLISM = 'pointillism'  # if found, presume processed

MD_BODY = """
[
![pointillism.io]({url}.svg?theme=auto)
]({url}.html)
"""

MD_FOOTER = """
Learn more about ![pointillism.io](https://pointillism.io).
"""


class RemodificationException(Exception):
    pass


def pointillism_url(repo: Repo, filename, branch='master'):
    return f"https://pointillism.io/{repo.owner}/{repo.project}/{branch}/{filename}"


def postpend(repo: Repo, docfile='README.md', body=MD_BODY):
    """add `body` to the bottom of `docfile`"""
    if repo.path is None:
        raise Exception("Path not set on repo")

    dots = get_dotfiles(repo)
    logging.info(f"Found {len(dots)} dots.")
    with open(path.join(repo.path, docfile), "r") as readme:
        content = readme.read()
        if POINTILLISM in content:
            raise RemodificationException(
                f"{POINTILLISM} found in document: {docfile}")

    with open(path.join(repo.path, docfile), "a") as readme:
        for dot in dots:
            url = pointillism_url(repo, dot)
            readme.write(body.format(url=url))
        readme.write(MD_FOOTER)

    return True
