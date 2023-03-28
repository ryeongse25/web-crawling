from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import telepot
import os

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, 'sba.txt')

f = open('/home/ubuntu/crawling/token.txt', mode='rt', encoding='utf-8')
bot_token = f.read().splitlines()[0]
bot = telepot.Bot(bot_token)
chat_id = '-1001835326415'

CONTENT_LINK = 'https://www.sba.seoul.kr/Pages/ContentsMenu/Company_Support_Detail.aspx?RID='

# 마지막 페이지
def getLastPage(soup):
    last_page_tag = soup.select('#pagination span:last-child')[0].text
    last_page = ''.join(filter(str.isdigit, last_page_tag))
    return int(last_page)

# 타이틀 가져오기
def getTitle(soup):
    titles = soup.find_all('h3', {'class': 'ellipsis_any'})
    return titles

# 텔레그램 메세지 전송
def sendByTelegram(str):
    bot.sendMessage(chat_id, str)


def main():
    url = "https://www.sba.seoul.kr/Pages/ContentsMenu/Company_Support.aspx?C=6FA70790-6677-EC11-80E8-9418827691E2" 
    driver.get(url)
    time.sleep(2)

    last_page = 3

    old_sba = set()

    # 파일 읽기
    try:
        with open(file_path, 'r') as f:
            old_sba = set(f.read().splitlines())
    except FileNotFoundError:
        pass
    

    # 파일 쓰기
    with open(file_path, 'a') as f:
        for i in range(1, last_page + 1):
            driver.execute_script(f"javascript:pageMove({i})")
            time.sleep(2)

            titles = getTitle(BeautifulSoup(driver.page_source, 'html.parser'))
            for title in titles:
                if title.text.strip() not in old_sba:
                    content_id = title.parent.get('href').split("'")[1]
                    link = CONTENT_LINK + content_id
                    sendByTelegram(title.text.strip() + "\n" + link)
                    f.write(title.text.strip() + '\n')

        driver.quit()


if __name__ == "__main__":
    main()
