import time

from selenium import webdriver
# from data.config import fc_pass,fc_email

options = webdriver.FirefoxOptions()
options.set_preference("general.useragent.override","Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0")
driver = webdriver.Firefox(executable_path="E:\Lessons\TelegramBot\selenium\firefox\geckodriver.exe",options=options)


def open_ins():
    try:
        driver.get(url="https://instagram.com/")
        time.sleep(5)
        # username_input = driver.find_element()

    except Exception as err:
        print(err)
    finally:
        driver.close()
        driver.quit()