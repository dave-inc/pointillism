from base64 import b64decode
from github import Github
from config import (
    GITHUB_CLIENT_ID, GITHUB_SECRET, LDAP_HOST,
    DEFAULT_USER, DEFAULT_TOKEN
)

from point.models import GitHubUser

# TODO token could be passed by config
if LDAP_HOST is not None:
    DEFAULT_USER = GitHubUser.first(DEFAULT_USER)
    if DEFAULT_USER:
        DEFAULT_TOKEN = DEFAULT_USER.git_token


class GitContent:
    def __init__(self, creds=None):
        if hasattr(creds, 'git_token'):
            creds = creds.git_token
        elif DEFAULT_TOKEN:
            creds = DEFAULT_TOKEN

        self.github = Github(login_or_token=creds, client_id=GITHUB_CLIENT_ID,
                             client_secret=GITHUB_SECRET)

    def get_by_branch_path(self, owner, repo, branch_path):
        branch, *rest = branch_path.split('/')
        branches = repo.get_branches()
        path = ''
        for d in rest:
            if branch not in branches:
                branch += "/" + d
            else:
                path += '/' + d

        repo = self.github.get_repo(f'{owner}/{repo}', lazy=False)
        return b64decode(repo.get_contents(path, ref=branch).content).decode('utf-8')

    def get(self, owner, repo, branch, path):
        repo = self.github.get_repo(f'{owner}/{repo}', lazy=False)
        return b64decode(repo.get_contents(path, ref=branch).content).decode('utf-8')

    def owner(self, owner, repo):
        try:
            repo = self.github.get_repo(f'{owner}/{repo}', lazy=False)
            if repo:
                return repo.owner.login
        except Exception:
            return
