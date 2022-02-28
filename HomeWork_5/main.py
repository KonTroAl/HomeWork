"""
Вариант I
Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и сложить данные о письмах в базу данных:
- от кого
- дата отправки
- тема письма
- текст письма полный

Логин тестового ящика: study.ai_172@mail.ru
Пароль тестового ящика: NextPassword172#

Вариант II
2) Написать программу, которая собирает товары «В тренде» с сайта техники mvideo и складывает данные в БД. Сайт можно выбрать и свой. Главный критерий выбора: динамически загружаемые товары
"""

"""
Вариант I
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
from pprint import pprint
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as dke


def letter_link_collect():
    href_list = []

    for i in range(5):
        letters = driver.find_elements(By.XPATH,
                                       "//div[contains(@class, 'ReactVirtualized__Grid__innerScrollContainer')]/a")
        for letter in letters:
            if letter in href_list:
                pass
            else:
                href_list.append(letter.get_attribute('href'))
        actions = ActionChains(driver)
        actions.move_to_element(letters[-1])
        actions.perform()
        time.sleep(2)
    return href_list


def letter_info_search(href_list):
    count_of_letters = 0
    start_id = 0

    for href in href_list:
        driver.get(href)

        letter_dict = {}

        letter_dict['_id'] = start_id

        time.sleep(5)
        letter_dict['letter_link'] = href

        # letter_contact_el = driver.find_element(By.CLASS_NAME, "letter-contact")
        # letter_contact = driver.find_element(By.CLASS_NAME, "letter-contact").text
        letter_dict['letter_contact'] = driver.find_element(By.CLASS_NAME, "letter-contact").text

        # letter_date_el = driver.find_element(By.CLASS_NAME, "letter__date")
        # letter_date = driver.find_element(By.CLASS_NAME, "letter__date").text
        letter_dict['letter_date'] = driver.find_element(By.CLASS_NAME, "letter__date").text

        # letter_header_el = driver.find_element(By.CLASS_NAME, 'thread-subject')
        # letter_header = driver.find_element(By.CLASS_NAME, 'thread-subject').text
        letter_dict['letter_header'] = driver.find_element(By.CLASS_NAME, 'thread-subject').text

        # letter_text = driver.find_element(By.XPATH, "//div[@class='letter__body']//table")

        letter_dict['letter_text'] = driver.find_element(By.XPATH, "//div[@class='letter__body']//table | //div[@class='letter__body']//div[@class='content_mr_css_attr']").text

        try:
            db_list = []

            db_dict = letters_collection.find({})

            if db_dict:
                for doc in db_dict:
                    db_list.append(doc['letter_link'].split('/?')[0])

                last_id = len(db_list)
                # print(letter_dict['letter_link'])
                # print(db_list[12])

                if letter_dict['letter_link'].split('/?')[0] in db_list:
                    pass
                else:
                    letter_dict['_id'] = last_id
                    letters_collection.insert_one(letter_dict)
                    count_of_letters += 1
            else:
                letters_collection.insert_one(letter_dict)
                count_of_letters += 1
        except dke:
            pass

    return count_of_letters


if __name__ == '__main__':


    client = MongoClient('localhost', 27017)
    db = client['news_db']
    letters_collection = db.letters

    chrome_options = Options()
    chrome_options.add_argument('start-maximized')

    s = Service('./chromedriver.exe')
    driver = webdriver.Chrome(service=s, options=chrome_options)

    url = 'https://account.mail.ru/login?page=https%3A%2F%2Fe.mail.ru%2Fmessages%2Finbox%3Futm_source%3Dportal%26utm_medium%3Dmailbox%26utm_campaign%3De.mail.ru%26mt_click_id%3Dmt-veoz41-1645947375-108968048&allow_external=1'

    driver.get(url)

    login = 'study.ai_172@mail.ru'
    password = 'NextPassword172#'

    wait = WebDriverWait(driver, 10)
    elem = wait.until(EC.presence_of_element_located((By.NAME, "username")))

    elem.send_keys(login)
    elem.send_keys(Keys.ENTER)

    elem = wait.until(EC.presence_of_element_located((By.NAME, "password")))
    time.sleep(1)
    elem.send_keys(password)
    elem.send_keys(Keys.ENTER)

    time.sleep(5)

    print(f'В базу данных писем добавлено: {letter_info_search(letter_link_collect())}')

    driver.close()
