from os import environ
import logging
from . import find_dot_repos

logging.basicConfig(level=logging.DEBUG,
                    filename="logs/github_search.log",
                    format="%(asctime)s:%(levelname)s:%(message)s"
                    )
logging.getLogger().addHandler(logging.StreamHandler())

# NOTE: No TARGET_USER searches for most recent.
find_dot_repos(environ.get("TARGET_USER"))
