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

chrome_options = Options()
chrome_options.add_argument('start-maximized')

s = Service('./chromedriver.exe')
driver = webdriver.Chrome(service=s, options=chrome_options)
# driver.implicitly_wait(10)

url = 'https://account.mail.ru/login?page=https%3A%2F%2Fe.mail.ru%2Fmessages%2Finbox%3Futm_source%3Dportal%26utm_medium%3Dmailbox%26utm_campaign%3De.mail.ru%26mt_click_id%3Dmt-veoz41-1645947375-108968048&allow_external=1'

driver.get(url)

login = 'study.ai_172@mail.ru'
password = 'NextPassword172#'

wait = WebDriverWait(driver, 10)
elem = wait.until(EC.presence_of_element_located((By.NAME, "username")))

elem.send_keys(login)
elem.send_keys(Keys.ENTER)

elem = wait.until(EC.presence_of_element_located((By.NAME, "password")))
time.sleep(2)
elem.send_keys(password)
elem.send_keys(Keys.ENTER)

print()
href_list = []

time.sleep(5)

for i in range(5):
    letters = driver.find_elements(By.XPATH, "//div[contains(@class, 'ReactVirtualized__Grid__innerScrollContainer')]/a")
    for letter in letters:
        if letter in href_list:
            pass
        else:
            href_list.append(letter.get_attribute('href'))
    actions = ActionChains(driver)
    actions.move_to_element(letters[-1])
    actions.perform()
    time.sleep(2)

driver.get(href_list[0])

letter_dict = {}
"""
- от кого
- дата отправки
- тема письма
- текст письма полный
"""

time.sleep(5)
letter_dict['letter_link'] = href_list[0]
letter_contact_el = driver.find_element(By.CLASS_NAME, "letter-contact")
letter_contact = letter_contact_el.text
letter_dict['letter_contact'] = letter_contact

letter_date_el = driver.find_element(By.CLASS_NAME, "letter__date")
letter_date = letter_date_el.text
letter_dict['letter_date'] = letter_date

letter_header_el = driver.find_element(By.CLASS_NAME, 'thread-subject')
letter_header = letter_header_el.text
letter_dict['letter_header'] = letter_header

letter = []
letter_text_el = driver.find_elements(By.XPATH, "//div[@class='letter__body']//table//span")
for item in letter_text_el:
    letter.append(item.text)

letter_dict['letter_text'] = letter

pprint(letter_dict)
driver.close()
