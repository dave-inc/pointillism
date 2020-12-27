import logging
from os import path
from glob import glob
from prmonster import Repo

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


def update_readmes(repo: Repo):
    if repo.path is None:
        raise Exception("Path not set on repo")

    # TODO only checking root level
    dots = glob(path.join(repo.path, "*.dot")) + \
           glob(path.join(repo.path, "*.gv")) + \
           glob(path.join(repo.path, "**/*.dot"), recursive=True) + \
           glob(path.join(repo.path, "**/*.gv"), recursive=True)
    logging.info(f"Found {len(dots)} dots.")
    for dot_file in dots:
        dot_path = path.join(repo.path, dot_file)
        logging.info(f"opening {dot_path}")
        with open(dot_path, "r") as readme:
            content = readme.read()
            if POINTILLISM in content:
                raise RemodificationException(
                    f"{POINTILLISM} found in document: README.md")

        with open(dot_path, "a") as readme:
            for dot in dots:
                url = pointillism_url(repo, dot)
                readme.write(MD_BODY.format(url=url))
            readme.write(MD_FOOTER)

def find_docs(repo: Repo):
    if repo.path is None:
        return None
    return glob(path.join(repo.path, "*.md"), recursive=True) +\
           glob(path.join(repo.path, "*.rst"), recursive=True)
