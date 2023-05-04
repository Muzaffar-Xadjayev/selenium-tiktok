import logging
import os
import sys
import time

import fake_useragent
from playhouse.shortcuts import model_to_dict
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc
from selenium.webdriver.common.action_chains import ActionChains
from database.models import *
import pickle

class TikTokBot:
    def __init__(self,fc_password,fc_email):
        self.fc_password = fc_password
        self.fc_email = fc_email

        # options = webdriver.ChromeOptions()
        user_agent = fake_useragent.UserAgent()
        # options.add_argument(
        #     f"user-agent={user_agent.random}", )
        # options.set_capability("dom.webdriver.enabled", False)
        # self.driver = webdriver.Chrome(
        #     executable_path="E:\Lessons\TelegramBot\selenium\chrome\chromedriver.exe",
        #     options=options
        # )

        options = webdriver.ChromeOptions()
        options.add_argument(f"user-agent={user_agent.random}")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        self.driver = uc.Chrome(use_subprocess=True, headless=False, driver_executable_path="chrome/chromedriver.exe")

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
        if os.path.exists(f'.\cookies\{self.fc_email.split("@")[0]}_cookie'):
            print("Cookies exists! You can log in")
            self.driver.get("https://tiktok.com/")
            self.driver.implicitly_wait(15)
            for cookie in pickle.load(open(f".\cookies\{self.fc_email.split('@')[0]}_cookie", "rb")):
                self.driver.add_cookie(cookie)
            time.sleep(5)
            self.driver.refresh()
            time.sleep(60)
            print("cookie qushilib, refresh buldi")
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
                    self.driver.implicitly_wait(15)
                    # time.sleep(5)

                    # self.driver.find_element(By.CLASS_NAME, "tiktok-1prdlp9-DivBoxContainer").click()
                    fc = self.driver.find_elements(By.XPATH, "//*[contains(@class, 'DivBoxContainer')]")
                    print(fc)
                    for i in fc:
                        if "Facebook" in i.text:
                            i.click()
                            break

                    print("facebookni bosdi")
                    time.sleep(5)
                    self.driver.implicitly_wait(10)

                    self.driver.switch_to.window(self.driver.window_handles[1])
                    time.sleep(5)
                    #
                    email_input = self.driver.find_element(By.NAME, 'email')
                    email_input.clear()
                    email_input.send_keys(self.fc_email)
                    print("email kiritildi")
                    time.sleep(3)
                    self.driver.implicitly_wait(10)
                    #
                    password_input = self.driver.find_element(By.NAME, 'pass')
                    password_input.clear()
                    password_input.send_keys(self.fc_password, Keys.ENTER)
                    print("pass kiritildi")
                    time.sleep(10)
                    self.driver.implicitly_wait(10)

                    self.driver.switch_to.window(self.driver.window_handles[0])
                    time.sleep(20)

                    print("tugadi")
                    pickle.dump(self.driver.get_cookies(), open(f'E:\Lessons\TelegramBot\selenium\cookies\{self.fc_email.split("@")[0]}_cookie', 'wb'))
                    time.sleep(5)
                except Exception as er:
                    logging.info(er)
            else:
                print("Ooopps,")

    def reply_comment(self):
        check_login_btn_exists = self.selector_exists("#header-login-button")
        if check_login_btn_exists:
            print("you couldn't login")
        else:
            print("Login successfully")




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
    # tiktok_bot = TikTokBot(fc_password=call_db_for_password()[0],fc_email=call_db_for_email()[0])
    tiktok_bot = TikTokBot(fc_password="your_pass",fc_email="your_email")
    tiktok_bot.get_cookies()
    # time.sleep(10)
    # tiktok_bot.reply_comment()

if __name__ == "__main__":
    main()
