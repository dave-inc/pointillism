#
# GH file search client
# https://docs.github.com/en/free-pro-team@latest/rest/reference/search
#
import logging
from config import PROJECT_ROOT
from datetime import datetime
from time import sleep
from .search import *

logging.basicConfig(filename="/var/log/pointillism.prmonster.log")
log = logging.getLogger().info

NOW = datetime.strftime(datetime.now(), "%Y-%m-%d")
REPO_DOC_PATH = PROJECT_ROOT + '/logs/repos'
REPORT_PATH = f"{REPO_DOC_PATH}/reports/dailyreport-{NOW}.md"

CLIENT = GitHubFileSearchClient()
CONTENT = GitHubContent()
PAGE_MAX = 100
SUPPORTED_DOCS = ('md',) # , 'rst')
TAB = "\t"


def log_repos(target_repos):
    log("======= discovered ======")
    for target in target_repos:
        if target[1] is None:
            log(TAB.join(map(str, ["DISCOVERED",
                                   target[0],
                                   "",
                                   "",
                                   *map(lambda i: i.content_url(), target[2:])
                                   ]
                             )))
        else:
            log(TAB.join(map(str, ["DISCOVERED",
                                   target[0],
                                   target[1].content_url(),
                                   target[1].url,
                                   *map(lambda i: i.content_url(), target[2:])
                                   ]
                             )))


def record_repo(owner, project, repo, dots, dot_refs, author, target_docs, unsupported):
    fp = open(f'{REPO_DOC_PATH}/{owner}-{project}', 'w')
    record = lambda msg: fp.write(f"{msg}\n")
    record("=========================")
    record(f"PROCESSING REPO: {repo} dots: {len(dots)} refs: {len(dot_refs.items)} {author}")
    record("========= dots ==========")
    for dot in dots:
        record(str(dot))
    record("== dot file references ==")
    for ref in target_docs + unsupported:
        record(str(ref))
    fp.close()


class RepoReport:
    def __init__(self, repo, dots, dot_refs, author):
        self.repo = repo
        self.dots = dots
        self.dot_refs = dot_refs
        self.author = author

    def save(self):
        report = open(REPORT_PATH, 'w')
        report.write(datetime.strftime(datetime.now(),
                                       "# Report: %Y-%m-%d\n\n"))
        report.write("## Repos\n\n")
        report.write("| repo | dots | refs | author | link |\n")
        report.write("| ---- | ---- | ---- | ------ | ---- |\n")

        for report in self.reports:
            report.write(f"| {repo} | {len(dots)} | {len(dot_refs.items)} | {author}| [link](https://github.com/{repo}) |\n")

        report.write("\n")
        report.write("Repo Count: %s\n", str(repo_count))
        report.close()


def find_dot_repos(user=None):
    repo_count = 0
    target_repos = []
    page = 0
    report = open(REPORT_PATH, 'w')
    report.write(datetime.strftime(datetime.now(),
                                   "# Report: %Y-%m-%d\n\n"))
    report.write("## Repos\n\n")
    report.write("| repo | dots | refs | author | link |\n")
    report.write("| ---- | ---- | ---- | ------ | ---- |\n")

    while page < PAGE_MAX:
        args = {}
        if user is not None:
            args['user'] = user

        resp = CLIENT.search(DOT_FILE_SEARCH, page, **args)
        logging.info(resp)
        if not resp.repos():
            break

        for repo in resp.repos():
            owner, project = repo.split('/')
            dots = list(filter(lambda i: repo == i.repo, resp.items))
            author = ":".join(list(CONTENT.last_author(repo).values()))

            repo_count += 1
            target_docs = []
            unsupported = []

            dot_refs = CLIENT.search("*.png", repo=repo)
            # + CLIENT.search("*.svg", repo=repo)
            if not dot_refs:
                target_repos.append([repo, None
                                     ] + dots)
            for ref in dot_refs.items:
                if ref.filetype() in SUPPORTED_DOCS:
                    target_docs.append(ref)
                    target_repos.append([repo,
                                         ref
                                         ] + dots)
                else:
                    unsupported.append(ref)

            report.write(f"| {repo} | {len(dots)} | {len(dot_refs.items)} | {author}| [link](https://github.com/{repo}) |\n")
            record_repo(owner, project, repo, dots, dot_refs, author, target_docs, unsupported)
        log_repos(target_repos)

        page += 1
        sleep(1)

    report.write("\n")
    report.write("Repo Count: %s\n", str(repo_count))
    report.close()

    with open(f'{REPO_DOC_PATH}/repo.counts', 'a+') as fp:
        fp.write(datetime.strftime(datetime.now(), "%Y-%m-%d"))
        fp.write("\t")
        fp.write(str(repo_count))
        fp.write("\n")
