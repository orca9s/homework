import os
import re
from urllib import parse
from bs4 import BeautifulSoup
import requests

url_webtoon_list = 'http://comic.naver.com/webtoon/weekday.nhn'
file_path = 'data/webtoon_list.html'
if os.path.exists(file_path):
    f = open(file_path, 'rt')
    html = f.read()
    f.close
else:
    # 파일이 없다면,
    # 웹툰 목록 url로부터 텍스트 데이터 받아와서 html변수에 할당하고
    # 텍스트 쓰기 모드로 파일을 열고 기록 후 닫는다.
    print('-파일이 없음({})'.format(file_path))
    response = requests.get(url_webtoon_list)
    print('-requests로 요청 완료')
    html = response.text
    print('-파일 쓰기 시작')
    f = open(file_path, 'wt')
    f.write(html)
    f.close()
    print('-파일 쓰기 완료')

response = requests.get(url_webtoon_list)
html = response.text

soup = BeautifulSoup(html, 'lxml')
# print('뷰티풀 소프 객체 생성 완료')

a_list = soup.select('a.title')

a_dict_list = []

for a in a_list:
    href = a.get('href')
    query_dict = parse.parse_qs(parse.urlsplit(href).query)
    webtoon_id = query_dict.get('titleId')[0]
    webtoon_title = a.string
    a_dict_list.append({
        'webtoon_id': webtoon_id,
        'title': webtoon_title,
    })

# for a_dict in a_dict_list:
#     print(a_dict['title'], a_dict['webtoon_id'])

a_text_list = []
for a in a_list:
    a_text_list.append(a.string)

a_text_list_set = set(a_text_list)
a_text_list = list(a_text_list_set)

search_result_list = []


def turn_on():
    print('취소하려면 control + c를 누르세요')
    choice = input('검색할 웹툰을 입력하세요:\n')
    for webtoon_title_list in a_text_list:
        if choice in webtoon_title_list:
            search_result_list.append(webtoon_title_list)
    if not search_result_list:
        print('찾는 웹툰이 없습니다.')
    else:
        print(search_result_list)

turn_on()

# search_result_list = [a_text for a_text in a_text_list if '노블' in a_text]
