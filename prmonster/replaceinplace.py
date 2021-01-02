import re
from prmonster import Repo

BRANCH = 'master'

def replace_dotrefs(repo: Repo, doc_content, dotfilename):
    # get after last slash, then split on dots
    *names, ext = dotfilename.split('/')[-1].split('.')
    name = ".".join(names)
    name_png = "\(([^\s]*\/{name}).png".format(name=name) #
    replacement = f"(https://pointillism.io/{repo.repo}/{BRANCH}/\\1.dot.png"
    return re.sub(name_png, replacement, doc_content)
