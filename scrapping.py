import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from data.config import fc_pass,fc_email
import pickle
from fake_useragent import UserAgent

useragent = UserAgent()
options = webdriver.FirefoxOptions()

# options.set_preference("general.useragent.override",f"Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0")
options.set_preference("general.useragent.override",f"{useragent.random}")

proxy = "138.128.91.65:8000"
firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
firefox_capabilities["marionette"] = True

firefox_capabilities["proxy"] = {
    "proxyType":"MANUAL",
    "httpProxy": proxy,
    "ftpProxy":proxy,
    "sslProxy":proxy
}

driver = webdriver.Firefox(executable_path="E:\Lessons\TelegramBot\selenium\firefox\geckodriver.exe",options=options,proxy=proxy)



def open_ins():
    try:
        # driver.get(url="https://www.tiktok.com/")
        # time.sleep(10)
        # login_btn = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div/div[3]/button')
        # time.sleep(3)
        # login_btn.click()
        # time.sleep(5)
        # window = driver.find_element(By.XPATH, '/html/body/div[7]/div[3]/div/div/div[1]/div[1]/div/div/div[1]')
        # time.sleep(3)
        # window.click()
        # time.sleep(5)
        # password = driver.find_element(By.XPATH, '/html/body/div/div[2]/form/div[1]/table/tbody/tr[1]/td/input')
        # password.send_keys(fc_pass)
        # time.sleep(3)
        # password.send_keys(Keys.ENTER)
        # time.sleep(5)
        # #
        # # # cookies
        # pickle.dump(driver.get_cookies(),open(f'{fc_pass}_cookie', "wb"))
        driver.get("https://2ip.ru")
        time.sleep(2)

        # for cookie in pickle.load(open(f"{ins_password}_cookie", "rb")):
        #     driver.add_cookie(cookie)
        #
        # time.sleep(5)
        # driver.refresh()
        # time.sleep(10)

    except Exception as err:
        print(err)
    finally:
        pass
        # driver.close()
        # driver.quit()

if __name__ == "__main__":
    # while True:
    open_ins()
