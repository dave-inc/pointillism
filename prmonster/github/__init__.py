#
# GH file search client
# https://docs.github.com/en/free-pro-team@latest/rest/reference/search
#
import logging
from config import PROJECT_ROOT
from datetime import datetime
from time import sleep
from .models import RepoReport
from .search import *
from prmonster import crm

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


def log_repo(owner, project, repo, dots, dot_refs, author, target_docs, unsupported, report):
    fp = open(f'{REPO_DOC_PATH}/{owner}-{project}', 'w')
    record = lambda msg: fp.write(f"{msg}\n")
    record(f"# REPO: {repo} dots: {len(dots)} refs: {len(dot_refs.items)} {author}")
    record(str(report))
    record("## dots\n\n")
    for dot in dots:
        record("- " + str(dot))
    record("## dot file references\n\n")
    for ref in target_docs + unsupported:
        record("- " + str(ref))
    fp.close()

def log_reports(reports): #  list[RepoReport]):
    fp = open(REPORT_PATH, 'w')
    fp.write(datetime.strftime(datetime.now(),
                               "# Report: %Y-%m-%d\n\n"))
    fp.write("## Repos\n\n")
    fp.write("| repo | followers | dots | refs | author |\n")
    fp.write("| ---- | --------- | ---- | ---- | ------ |\n")

    for report in reports:
        fp.write("| " + " | ".join(map(str, (
            f"[{report.repo.repo_s}](https://github.com/{report.repo.repo_s})",
            report.followers,
            len(report.dots),
            len(report.dot_refs.items),
            report.author,
            ))) + "\n")

    fp.write("\n")
    fp.write(f"Repo Count: {str(len(reports))}\n")
    fp.close()


def find_dot_repos(user=None):
    repo_count = 0
    target_repos = []
    page = 0
    resume = 0

    resp = None
    reports = []
    while page < PAGE_MAX:
        # try:
        # if resp is not None and resp.wait:
        #     logging.info(f"Waiting until {int(datetime.utcnow().timestamp())} > {resp.resume}")
        #     sleep(5)
        #     resume = resp.resume
        #     raise EnhanceCalm(f"Waiting until {int(datetime.utcnow().timestamp())} > {resp.resume}")
        args = {}
        if user is not None:
            args['user'] = user
        resp = CLIENT.search(DOT_FILE_SEARCH, page=page, **args)
        logging.info(resp)
        if not resp.repos():
            break

        for repo_s in resp.repos():
            repo_info = CONTENT.repo_info(repo_s)
            owner, project = repo_s.split('/')
            repo = crm.models.Repo(owner=owner, name=project,
                                   repo_info=repo_info)
            dots = list(filter(lambda i: repo_s == i.repo, resp.items))
            author = ":".join(list(CONTENT.last_author(repo_s).values()))
            repo_count += 1
            target_docs = []
            unsupported = []

            dot_refs = CLIENT.search("*.png", repo=repo_s)  # + CLIENT.search("*.svg", repo=repo_s)
            if not dot_refs:
                target_repos.append([repo_s, None] + dots)
            for ref in dot_refs.items:
                if ref.filetype() in SUPPORTED_DOCS:
                    target_docs.append(ref)
                    target_repos.append([repo_s,
                                         ref
                                         ] + dots)
                else:
                    unsupported.append(ref)

            report = RepoReport(repo, dots, dot_refs, author, repo_info)
            reports.append(report)

            for report in reports:
                crm.save_report(report)
            log_reports(reports)
            log_repo(owner, project, repo_s, dots, dot_refs, author, target_docs, unsupported, report)
            sleep(15)
        page += 1
        sleep(1)
        # except EnhanceCalm as err:
        #     logging.info(err)


    with open(f'{REPO_DOC_PATH}/repo.counts', 'a+') as fp:
        fp.write(datetime.strftime(datetime.now(), "%Y-%m-%d"))
        fp.write("\t")
        fp.write(str(len(reports)))
        fp.write("\n")
