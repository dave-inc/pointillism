#
# GH file search client
# https://docs.github.com/en/free-pro-team@latest/rest/reference/search
#
import logging
from time import sleep
from .search import *

CLIENT = GitHubFileSearchClient()
PAGE_MAX = 100

def find_dot_repos():
    page = 0
    while page < PAGE_MAX:
        resp = CLIENT.search(DOT_FILE_SEARCH, page)
        logging.info(resp)
        if not resp.repos():
            break

        dot_names = [item.filename() for item in resp.items]

        for repo in resp.repos():
            logging.info("=========================")
            logging.info(repo)
            dots = filter(lambda i: repo == i.repo, resp.items)
            for dot in dots:
                logging.info(dot)
            dot_refs = CLIENT.search("*.png", repo=repo)
            logging.info("dot file references")
            for ref in dot_refs.items:
                if ref.filename() in dot_names:
                    logging.info(f"{ref}\t{ref.filename()}\t{ref.filetype()}")
                else:
                    logging.info(ref)

        page += 1
        sleep(1)
