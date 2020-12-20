import logging
from time import sleep
from . import GitHubFileSearchClient

logging.basicConfig(level=logging.DEBUG, filename="github_search.log")

client = GitHubFileSearchClient()

page = 0
while page < 100:
    resp = client.search(page)
    logging.info(resp)
    for item in resp.items:
        logging.info(item)

    page += 1
    sleep(1)