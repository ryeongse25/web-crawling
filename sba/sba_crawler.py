from selenium import webdriver
from bs4 import BeautifulSoup
import time
import telepot
import os
from dotenv import load_dotenv

load_dotenv('../.env')

driver = webdriver.Chrome(executable_path = os.environ['DRIVER_PATH'])

bot_token = os.environ['BOT_TOKEN']
bot = telepot.Bot(bot_token)

# chat_id = bot.getUpdates()[-1]['message']['chat']['id']
chat_id = os.environ['CHAT_ID']

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

    last_page = getLastPage(BeautifulSoup(driver.page_source, 'html.parser'))

    old_sba = set()

    # 파일 읽기
    try:
        with open('sba.txt', 'r') as f:
            old_sba = set(f.read().splitlines())
    except FileNotFoundError:
        pass
    

    # 파일 쓰기
    with open('sba.txt', 'a') as f:
        for i in range(1, last_page + 1):
            string = ''
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