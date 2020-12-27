#
# GH file search client
# https://docs.github.com/en/free-pro-team@latest/rest/reference/search
#
import logging
from time import sleep
from .search import *

log = logging.getLogger().info

CLIENT = GitHubFileSearchClient()
PAGE_MAX = 100
SUPPORTED_DOCS = ('md',) # , 'rst')
TAB = "\t"


def find_dot_repos(user):
    target_repos = []
    page = 0
    while page < PAGE_MAX:
        args = {}
        if user is not None:
            args['user'] = user
        resp = CLIENT.search(DOT_FILE_SEARCH, page, **args)
        logging.info(resp)
        if not resp.repos():
            break

        dot_names = [item.filename() for item in resp.items]

        for repo in resp.repos():
            log("=========================")
            log(repo)
            dots = list(filter(lambda i: repo == i.repo, resp.items))

            log("========= dots ==========")
            for dot in dots:
                log(dot)

            log("== dot file references ==")
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
            for ref in target_docs + unsupported:
                log(ref)

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

        page += 1
        sleep(1)
