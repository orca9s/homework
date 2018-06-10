import os
import sys
from urllib import parse

import requests
from bs4 import BeautifulSoup

from finaltest import Webtoon

# finaltest의 유틸 실행 파일 이 파일이 있어야 모듈기능이 작동함

def search_webtoon(keyword):
    #  전체 웹툰에서 제목, titleId 가져오는 크롤링
    file_path = 'data/webtoon_list.html'
    webtoon_url = 'http://comic.naver.com/webtoon/weekday.nhn'

    if not os.path.exists(file_path):
        response = requests.get(webtoon_url)
        html = response.text
        open(file_path, 'wt').write(html)

    else:
        html = open(file_path, 'rt').read()

    soup = BeautifulSoup(html, 'lxml')
    a_list = soup.select('a.title')

    # 대학입력시 해당 키워드를 가지고 있는 웹툰 title와 웹툰 titleId
    result_list = list()
    webtoon_id_set = set()

    for a in a_list:
        href = a.get('href')
        query_string = parse.urlsplit(href).query
        query_dict = dict(parse.parse_qsl(query_string))
        webtoon_id = query_dict.get('titleId')
        title = a.get_text(strip=True)

        # 검색 키워드가 title이 포함되는 경우
        if keyword in title:
            # webtoon_id가 중복되는 경우 continue
            if webtoon_id in webtoon_id_set:
                # print(f'중복되는 웹툰:{webtoon_id}')
                continue

            webtoon_id_set.add(webtoon_id)
            # list에 webtoon_id와 title을 딕셔너리 형태로 추가
            result_list.append({
                'webtoon_id': webtoon_id,
                'title': title,
            })

    return result_list


def ini():
    # 검색할 웹툰명 입력
    search_keyword = input('검색할 웹툰명을 입력해주세요 :')

    # 입력받은 키워드를 통해 search_webtoon 함수 실행
    result_list = search_webtoon(search_keyword)

    # 선택할 수 있는 웹툰 리스트를 출력
    for num, webtoon in enumerate(result_list):
        print(f'{num}: {webtoon["title"]}')
    # 사용자가 원하는 웹툰 번호 입력
    select_webtoon = input("선택 :")

    # result_list = [{"webtoon_id":"312121","title":"신의 탑"},{}]
    # 사용자가 선택한 번호를 통해 result_list에서 원하는 만화 정보를 가져옴
    # result_list[1]["webtoon_id"] 라는 key값의 value를 뽑아옴
    # print(result_list[int(select_webtoon)]["webtoon_id"])
    webtoon1 = Webtoon(webtoon_id=result_list[int(select_webtoon)]['webtoon_id'])

    select_webtoon_menu(webtoon1)


def select_webtoon_menu(webtoon):
    while True:
        print('------------------------------------------')
        print(f'현재 {webtoon.title} 웹툰이 선택되어 있습니다.')
        print('1. 웹툰 정보 보기')
        print('2. 웹툰 저장하기')
        print('3. 다른 웹툰 검색해서 선택하기')
        print('4. 종료하기')
        select_menu = input('선택 :')

        if select_menu is '1':
            print('------------------------------------------')
            print(webtoon.show_info())
        elif select_menu is '2':
            pass
        elif select_menu is '3':
            ini()
        elif select_menu is '4':
            sys.exit(1)
        else:
            print('올바른 입력이 아닙니다. 다시 선택해주세요')


if __name__ == '__main__':
    ini()
