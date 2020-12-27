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
    dots = glob(path.join(repo.path, "*.dot")) + \
           glob(path.join(repo.path, "*.gv"))

    if dots:
        with open(path.join(repo.path, "README.md"),
                  "a") as readme:
            content = readme.read()
            if POINTILLISM in content:
                raise RemodificationException(
                    f"{POINTILLISM} found in document: README.md")



            for dot in dots:  # TODO only one level
                url = pointillism_url(repo, dot)
                readme.write(MD_BODY.format(url=url))
            readme.write(MD_FOOTER)
