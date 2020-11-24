from os import path
from base64 import b64decode
import subprocess
from prmonster import Repo
from github import Github

CHECKOUT_DIR = "/tmp/pointillism_prs"

GITHUB = Github(login_or_token='d2be3d90f88e0bbf64e79a009cc5f030ff2910fc')
BRANCH = "pointillism"

def github_url(repo: Repo):
    return f"git@github.com:{repo.owner}/{repo.project}.git"

def checkout_path(repo: Repo):
    return path.join(
       CHECKOUT_DIR, repo.owner, repo.project
    )

def contents(repo: Repo, filepath: str='README.md'):
    """get contents of a repo file"""
    ghrepo = GITHUB.get_repo(repo.repo)
    return b64decode(ghrepo.get_contents(filepath).content).decode('utf-8')

def checkout(repo: Repo):
    subprocess.run(["mkdir", "-p", checkout_path(repo)],
                   check=True)
    subprocess.run(
        ['git',
         'clone',
         github_url(repo),
         checkout_path(repo)
         ],
        check=True
    )
    subprocess.run([
        'git',
        '-C',
        checkout_path(repo),
        'checkout',
        '-b', BRANCH
    ], check=True)

    repo.path = checkout_path(repo)
    return repo

def commit(repo: Repo, message: str):
    subprocess.run([
        'git',
        '-C',
        checkout_path(repo),
        'commit',
        '-a', '-m',
        message
    ], check=True)

def pr(repo: Repo):
    """submit a PR of outstanding changes."""
    ghrepo = GITHUB.get_repo(repo.repo)

    subprocess.run([
        'git',
        '-C',
        checkout_path(repo),
        'push',
        'origin',
        '-u',
        BRANCH
    ], check=True)
    ghrepo.create_pull(
        title="pointillism.io Auto-Documentation Update",
        base="master",
        head=BRANCH,
        body="""
        Adding pointillism.io images to `README.md`.
        
        pointillism.io makes it easy to document your projects
        using markdown, without setting up any infrastructure.
        
        Learn more at [pointillism.io](https://pointillism.io).
        """
    )
