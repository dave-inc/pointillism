from glob import glob


MD_BODY = """
[
![pointillism.io]({url}.svg?theme=auto)
]({url}.html)
"""

MD_FOOTER = """
Learn more about ![pointillism.io](https://pointillism.io).
"""


def pointillism_url(owner, repo, filename, branch='master'):
    return f"https://pointillism.io/{owner}/{repo}/{branch}/{filename}"


def update_readmes():
    owner = 'trevorgrayson'
    repo = 'pointillism'
    dots = glob("*.dot") + glob("*.gv")

    if dots:
        with open("README.md", "a") as readme:
            for dot in dots:  # only one level
                url = pointillism_url(owner, repo, dot)
                readme.write(MD_BODY.format(url=url))
            readme.write(MD_FOOTER)

