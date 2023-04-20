import logging
import os
import sys
import time

from playhouse.shortcuts import model_to_dict
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from database.models import *
import pickle

class TikTokBot:
    def __init__(self,fc_password,fc_email):
        self.fc_password = fc_password
        self.fc_email = fc_email

        options = webdriver.ChromeOptions()

        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36", )
        options.set_capability("dom.webdriver.enabled", False)
        self.driver = webdriver.Chrome(
            executable_path="E:\Lessons\TelegramBot\selenium\chrome\chromedriver.exe",
            options=options
        )

    def selector_exists(self,selector):
        try:
            self.driver.find_element(By.CSS_SELECTOR, selector)
            exists = True
        except NoSuchElementException:
            exists = False

        return exists

    def check_xpath(self,xpath):
        try:
            self.driver.find_element(By.XPATH, xpath)
            exists = True
        except NoSuchElementException:
            exists = False

        return exists



    def close_driver(self):
        self.driver.close()
        self.driver.quit()

    def get_cookies(self):
        if os.path.exists(f'E:\Lessons\TelegramBot\selenium\cookies\{call_db_for_email()[0].split("@")[0]}_cookie'):
            print("Cookies exists! You can log in")
            self.driver.get("https://tiktok.com/")
            self.driver.implicitly_wait(15)
            for cookie in pickle.load(open(f"E:\Lessons\TelegramBot\selenium\cookies\{call_db_for_email()[0].split('@')[0]}_cookie", "rb")):
                self.driver.add_cookie(cookie)
            time.sleep(3)
            self.driver.refresh()
            time.sleep(55)

        else:
            print("No Cookies! Trying to log in")
            self.driver.get("https://tiktok.com/")
            self.driver.implicitly_wait(15)

            if self.selector_exists("#header-login-button"):
                try:
                    pp = self.selector_exists(".tiktok-aiuhe9-DivModalContent")
                    print(pp)
                    if pp:
                        time.sleep(3)
                        self.driver.implicitly_wait(5)
                        self.driver.find_element(By.CSS_SELECTOR,
                                            '#login-modal > div.tiktok-18x2367-DivCloseWrapper.e1gjoq3k6').click()
                    else:
                        print("Modal oyna yo'q")
                    print("pasga utdi")
                    time.sleep(5)
                    # self.driver.implicitly_wait(5)
                    # time.sleep(2)
                    self.driver.find_element(By.CSS_SELECTOR, '#header-login-button').click()
                    print("login btn bosdi")
                    # self.driver.implicitly_wait(5)
                    # time.sleep(3)

                    # self.driver.find_element(By.CLASS_NAME, "tiktok-1prdlp9-DivBoxContainer").click()
                    # print("facebookni bosdi")
                    # time.sleep(20)
                    # self.driver.implicitly_wait(10)
                    #
                    # self.driver.switch_to.window(self.driver.window_handles[1])
                    # time.sleep(5)
                    # #
                    # email_input = self.driver.find_element(By.NAME, 'email')
                    # email_input.clear()
                    # email_input.send_keys(call_db_for_email()[0])
                    # print("email kiritildi")
                    # time.sleep(3)
                    #
                    # password_input = self.driver.find_element(By.NAME, 'pass')
                    # password_input.clear()
                    # password_input.send_keys(call_db_for_password()[0], Keys.ENTER)
                    # print("pass kiritildi")
                    # self.driver.implicitly_wait(10)
                    #
                    # # self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div/div[2]").click()
                    # # time.sleep(5)
                    #
                    # self.driver.switch_to.window(self.driver.window_handles[0])
                    time.sleep(120)

                    print("tugadi")
                    pickle.dump(self.driver.get_cookies(), open(f'E:\Lessons\TelegramBot\selenium\cookies\{call_db_for_email()[0].split("@")[0]}_cookie', 'wb'))
                    time.sleep(5)
                except Exception as er:
                    logging.info(er)
            else:
                print("Ooopps,")

def call_db_for_email():
    ls = Logins.select()
    logins = [model_to_dict(i) for i in ls]
    emails = []
    for i in logins:
        emails.append(i["username_or_email"])
    return emails

def call_db_for_password():
    ls = Logins.select()
    logins = [model_to_dict(i) for i in ls]
    passwords = []
    for i in logins:
        passwords.append(i["password"])
    return passwords


def main():
    call_db_for_email()
    call_db_for_password()
    tiktok_bot = TikTokBot(fc_password=call_db_for_password()[0],fc_email=call_db_for_email()[0])
    tiktok_bot.get_cookies()


if __name__ == "__main__":
    main()
