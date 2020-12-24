import logging
from time import sleep
from . import GitHubFileSearchClient, DOT_FILE_SEARCH

logging.basicConfig(level=logging.DEBUG, filename="github_search.log")

client = GitHubFileSearchClient()

page = 0
while page < 100:
    resp = client.search(DOT_FILE_SEARCH, page)
    logging.info(resp)
    for repo in resp.repos():
        logging.info("=========================")
        logging.info(repo)
        dots = filter(lambda i: repo == i.repo, resp.items)
        for dot in dots:
            logging.info(dot)
        dot_refs = client.search("*.png", repo=repo)
        logging.info("dot file references")
        for ref in dot_refs.items:
            logging.info(ref)

    page += 1
    sleep(1)