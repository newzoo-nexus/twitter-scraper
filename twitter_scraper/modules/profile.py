from requests_html import HTMLSession, HTML
from lxml.etree import ParserError

session = HTMLSession()


class Profile:
    """
        Parse twitter profile and split informations into class as attribute.

        Attributes:
            - name
            - username
            - likes_count
            - tweets_count
            - followers_count
            - following_count
    """

    def __init__(self, username):
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Referer": f"https://twitter.com/{username}",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062 Safari/537.36",
            "X-Twitter-Active-User": "yes",
            "X-Requested-With": "XMLHttpRequest",
            "Accept-Language": "en-US",
        }

        page = session.get(f"https://twitter.com/{username}", headers=headers)
        self.username = username
        self.__parse_profile(page)

    def __parse_profile(self, page):
        try:
            html = HTML(html=page.text, url="bunk", default_encoding="utf-8")
        except KeyError:
            raise ValueError(f'Oops! Either "{self.username}" does not exist or is private.')
        except ParserError:
            pass

        page_title = html.find("title")[0].text
        self.name = page_title[: page_title.find("(")].strip()

        # get stats table if available
        stats_table = None
        stats = None
        try:
            stats_table = html.find("table.profile-stats")[0]
            stats = stats_table.find("td div.statnum")
            if not stats:
                self.tweets_count = None
                self.following_count = None
                self.followers_count = None
        except:
            self.tweets_count = None
            self.following_count = None
            self.followers_count = None

        # get total tweets count if available
        try:
            self.tweets_count = int(stats[0].text.replace(",", ""))
        except:
            self.tweets_count = None

        # get total following count if available
        try:
            self.following_count = int(stats[1].text.replace(",", ""))
        except:
            self.following_count = None

        # get total follower count if available
        try:
            self.followers_count = int(stats[2].text.replace(",", ""))
        except:
            self.followers_count = None

        # get total like count if available
        try:
            q = html.find('li[class*="--favorites"] span[data-count]')[0].attrs["data-count"]
            self.likes_count = int(q)
        except:
            self.likes_count = None

    def to_dict(self):
        return dict(
            name=self.name,
            username=self.username,
            likes_count=self.likes_count,
            tweets_count=self.tweets_count,
            followers_count=self.followers_count,
            following_count=self.following_count,
        )

    def __dir__(self):
        return [
            "name",
            "username",
            "likes_count",
            "tweets_count",
            "followers_count",
            "following_count",
        ]

    def __repr__(self):
        return f"<profile {self.username}@twitter>"
