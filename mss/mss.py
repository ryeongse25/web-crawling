import time
import telepot
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

f = open('/home/ubuntu/crawling/token.txt', mode='rt', encoding='utf-8')
bot_token = f.read().splitlines()[0]
bot = telepot.Bot(bot_token)
chat_id = '-1001835326415'

def getLastPage(btn):
    last_page_tag = btn.get_attribute('onclick')
    last_page = ''.join(filter(str.isdigit, last_page_tag))
    return int(last_page)

def readFile():
    old_set = set()

    try:
        with open('mss.txt', 'r') as f:
            old_set = set(f.read().splitlines())
    except FileNotFoundError:
        pass

    return old_set

def getLink(str):
    number = str.split("'")[3]
    link = f'https://www.mss.go.kr/site/smba/ex/bbs/View.do?cbIdx=310&bcIdx={number}&parentSeq={number}'
    return link

def sendByTelegram(str):
    bot.sendMessage(chat_id, str)


def main():
    url = "https://www.mss.go.kr/site/smba/ex/bbs/List.do?cbIdx=310" 
    driver.get(url)

    last_page_btn = driver.find_element(By.CSS_SELECTOR, '.paging .last')
    last_page = 3

    old_set = readFile()

    with open('mss.txt', 'a') as f:

        for i in range(1, last_page + 1):
            driver.execute_script(f"javascript:doBbsFPag({i})")

            items = driver.find_elements(By.CSS_SELECTOR, 'td.subject')

            for item in items:
                a_tag = item.find_element(By.TAG_NAME, 'a')
                if a_tag.text not in old_set:
                    link = getLink(a_tag.get_attribute('onclick'))
                    sendByTelegram(a_tag.text + "\n" + link)
                    f.write(a_tag.text + '\n')

    driver.quit()


if __name__ == "__main__":
    main()
