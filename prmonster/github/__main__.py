import logging
from . import find_dot_repos

logging.basicConfig(level=logging.DEBUG, filename="github_search.log")

find_dot_repos()
