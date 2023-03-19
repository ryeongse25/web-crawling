import time
import telepot
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By

load_dotenv('../.env')

driver = webdriver.Chrome(executable_path = os.environ['DRIVER_PATH'])

bot_token = os.environ['BOT_TOKEN']
bot = telepot.Bot(bot_token)
chat_id = os.environ['CHAT_ID']

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
    last_page = getLastPage(last_page_btn)

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