import time
import telepot
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import os

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, 'iitp.txt')

f = open('/home/ubuntu/crawling/token.txt', mode='rt', encoding='utf-8')
bot_token = f.read().splitlines()[0]
bot = telepot.Bot(bot_token)
chat_id = '-1001835326415'

URL_1 = 'https://www.iitp.kr/kr/1/business/businessApiList.it?pageIndex='
URL_2 = '&pageSize=10&searchText=&searchField=all'


def getLastPage(link):
    query = link.split("?")[1]
    return int(query[10:12])


def readFile():
    old_set = set()

    try:
        with open(file_path, 'r') as f:
            old_set = set(f.read().splitlines())
    except FileNotFoundError:
        pass
    
    return old_set


def sendByTelegram(item):
    message = item.text + '\n' + item.get_attribute('href')
    bot.sendMessage(chat_id, message)


def main():
    url = "https://www.iitp.kr/kr/1/business/businessApiList.it" 
    driver.get(url)

    # option 선택 (현재 option 선택 후 다음 페이지 이동시 전체로 변경되는 홈페이지 자체 이슈 있음) 
    # select = Select(driver.find_element(By.ID, 'findStep'))
    # select.select_by_value('Receipt')

    # search_btn = driver.find_element(By.CSS_SELECTOR, '.area-search .btn-primary')
    # search_btn.click()

    last_page_btn = driver.find_element(By.CSS_SELECTOR, '.pagination .next_end')
    link = last_page_btn.get_attribute('href')
    last_page = 3

    old_set = readFile()

    # 파일 쓰기
    with open(file_path, 'a') as f:

        for i in range(0, last_page + 1):

            new_url = URL_1 + str(i) + URL_2
            driver.get(new_url)

            trs = driver.find_elements(By.CSS_SELECTOR, '.comment-group0')

            for tr in trs:

                # 빈 데이터 존재
                try:
                    item = tr.find_element(By.TAG_NAME, 'a')
                    if item.text not in old_set:
                        sendByTelegram(item)
                        f.write(item.text + '\n')
                except:
                    pass
        
    driver.quit()


if __name__ == "__main__":
    main()
