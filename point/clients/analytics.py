import logging
from urllib import parse
from http.client import HTTPSConnection
HOST = 'www.google-analytics.com'


class GAnalytics:
    def __init__(self):
        self.client = HTTPSConnection(HOST)

    def pageview(self, path, user_id=None, **params):
        print(self.url(path=path,
                              user_id=user_id))
        self.client.request("GET",
                            self.url(path=path,
                                     user_id=user_id)
                            )

    def url(self, path=None, user_id=None, **params):
        """
        # tid=UA-xxxxxxxxxx-2
        # t=event
        # ec=testCategory
        # ea=testAction
        # v=1
        # cid=12345678
        """
        p = (
            "tid=UA-165967713-1",
            "t=pageview",
            "v=1",
            "ec=services",
            "ea=render",
            f"dp={parse.quote(path)}"  # page path
        )
        if user_id is not None:
            p += ('cid', user_id)

        return "/collect?" + \
               "&".join(p)


if __name__ == '__main__':
    ga = GAnalytics()
    ga.pageview("/test", "123")

