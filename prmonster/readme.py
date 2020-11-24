from os import path
from glob import glob
from prmonster import Repo

MD_BODY = """
[
![pointillism.io]({url}.svg?theme=auto)
]({url}.html)
"""

MD_FOOTER = """
Learn more about ![pointillism.io](https://pointillism.io).
"""


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
            for dot in dots:  # TODO only one level
                url = pointillism_url(repo, dot)
                readme.write(MD_BODY.format(url=url))
            readme.write(MD_FOOTER)
