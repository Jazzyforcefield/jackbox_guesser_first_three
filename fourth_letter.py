from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ExpectedConditions

from string import ascii_uppercase

import sys
import time
import re

"""
Source: https://stackoverflow.com/questions/35370755/python-selenium-wait-till-any-text
"""
class wait_for_text_to_match(object):
    def __init__(self, locator, pattern):
        self.locator = locator
        self.pattern = re.compile(pattern)

    def __call__(self, driver):
        try:
            element_text = driver.find_element(*self.locator).text
            return self.pattern.search(element_text)
        except Exception:
            return False

def main():
    if (len(sys.argv) < 2):
        print(f'Usage: python3 { sys.argv[0] } [first-three-letters]')
        return 

    first_three = sys.argv[1]

    if (len(first_three) > 3):
        print(f'Invalid argument: { first_three }')
        return

    chrome_options = Options()
    chrome_options.add_experimental_option('detach', True)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get('https://jackbox.tv/')


    name_entry = driver.find_element(by=By.ID, value='username')
    code_entry = driver.find_element(by=By.ID, value='roomcode')
    join_button = driver.find_element(by=By.ID, value='button-join')
    status = driver.find_element(by=By.CSS_SELECTOR, value='.status')

    name_entry.click()
    name_entry.send_keys('Baes #1 Fan')

    code_entry.click()
    code_entry.send_keys(first_three)
    for c in ascii_uppercase:

        code_entry.send_keys(c)
        wait = WebDriverWait(driver, 1)
        wait.until(wait_for_text_to_match((By.CSS_SELECTOR, '.status'), r".+"))

        if (status.text != 'Room not found'):
            break

        code_entry.send_keys(Keys.BACKSPACE)

    code_entry.send_keys(Keys.RETURN)


if __name__ == '__main__':
    start_time = time.time()
    main()
    print(f'--- { time.time() - start_time } seconds ---')
