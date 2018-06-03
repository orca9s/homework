import os
from urllib import parse

import requests
from bs4 import BeautifulSoup


class Webtoon:
    def __init__(self, webtoon_id, no, url_thumbnail, title, rating, created_date, webtoon_title):
        self.webtoon_id = webtoon_id
        self.no = no
        self.url_thumbmail = url_thumbnail
        self.title = title
        self.rating = rating
        self.created_date = created_date
        self.webtoon_title = webtoon_title
        self._html=''
        self._title_html = ''

    def title_html(self):
        if not self._title_html:
            file_path = 'data/webtoon_title_list-{webtoon_title}.html'.format(webtoon_title=self.webtoon_title)
            url_title_list = 'http://comic.naver.com/webtoon/weekday.nhn'
            params = {
                'titleId': self.webtoon_id
            }
            if os.path.exists(file_path):
                html = open(file_path, 'rt').read()
            else:
                response = requests.get(url_title_list, params)
                print(response.url)
                html = response.text
                open(file_path, 'wt').write(html)
            self._title_html = html
        return self._title_html
        print(title_html)

    def html(self):
        if not self._html:
            file_path = 'data.episode_list-{webtoon_id}.html'.format(webtoon_id=self.webtoon_id)
            url_episode_list = 'http://comic.naver.com/webtoon/list.nhn'
            params = {
                'titleId': self.webtoon_id,
            }
            if os.path.exists(file_path):
                html = open(file_path, 'rt').read()
            else:
                response = requests.get(url_episode_list, params)
                print(response.url)
                html = response.text
                open(file_path, 'wt').write(html)
            self._html = html
        return self._html

if __name__ == '__main__':
    print(title)
