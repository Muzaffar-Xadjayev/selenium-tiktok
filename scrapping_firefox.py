import logging
import os
import sys
import time

import fake_useragent
from playhouse.shortcuts import model_to_dict
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc
from selenium.webdriver.common.action_chains import ActionChains
from database.models import *
import pickle

class TikTokBot:
    def __init__(self,password,username,text):
        self.password = password
        self.username = username
        self.text = text

        user_agent = fake_useragent.UserAgent()
        options = webdriver.ChromeOptions()
        options.add_argument(f"user-agent={user_agent.random}")
        # options.set_capability("dom.webdriver.enabled", False)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        self.driver = uc.Chrome(use_subprocess=True, headless=False, driver_executable_path="chrome/chromedriver.exe")
        self.driver.maximize_window()

        # service = Service("chrome/chromedriver.exe")
        # options = webdriver.ChromeOptions()
        # user_agent = fake_useragent.UserAgent()
        # options.add_argument(
        #     f"user-agent={user_agent.random}", )
        # options.set_capability("dom.webdriver.enabled", False)
        # self.driver = webdriver.Chrome(
        #     service=service,
        #     options=options
        # )
        # self.driver.maximize_window()

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
        if os.path.exists(f'.\cookies\{self.username.split("@")[0]}_cookie'):
            print("Cookies exists! You can log in")
            self.driver.get("https://www.tiktok.com/login/phone-or-email/email")
            self.driver.implicitly_wait(15)
            for cookie in pickle.load(open(f".\cookies\{self.username.split('@')[0]}_cookie", "rb")):
                self.driver.add_cookie(cookie)
            time.sleep(5)
            self.driver.refresh()
            time.sleep(30)
            self.driver.implicitly_wait(60)
            print("cookie qushilib, refresh buldi")
        else:
            print("No Cookies! Trying to log in")
            self.driver.get("https://www.tiktok.com/login/phone-or-email/email")
            self.driver.implicitly_wait(15)
            try:
                email_input = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/form/div[1]/input')
                email_input.clear()
                email_input.send_keys(self.username)
                print("email kiritildi")
                time.sleep(3)
                self.driver.implicitly_wait(10)
                #
                password_input = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/form/div[2]/div/input')
                password_input.clear()
                password_input.send_keys(self.password, Keys.ENTER)
                print("pass kiritildi")
                self.driver.implicitly_wait(10)

                # self.driver.switch_to.window(self.driver.window_handles[0])

                time.sleep(40)
                print("tugadi, cookie saqlandi")
                pickle.dump(self.driver.get_cookies(), open(f'E:\Lessons\TelegramBot\selenium\cookies\{self.username.split("@")[0]}_cookie', 'wb'))
                time.sleep(5)
            except Exception as er:
                logging.info(er)

    def reply_comment(self):
        check_login_btn_exists = self.selector_exists("#header-login-button")
        if check_login_btn_exists:
            print("you couldn't login")
            self.get_cookies()
        else:
            print("Login successfully")
            self.driver.implicitly_wait(15)
            profile_img = self.driver.find_element(By.ID, 'header-more-menu-icon')
            actions = ActionChains(driver=self.driver)
            actions.move_to_element(profile_img).perform()
            time.sleep(3)
            self.driver.implicitly_wait(5)
            show_profile = self.driver.find_element(By.XPATH,
                                                    '/html/body/div[1]/div[1]/div/div[3]/div[4]/div/ul/li[1]/a').click()
            print("profile bo'limiga utdi")
            time.sleep(20)
            try:
                all_videos = self.driver.find_elements(By.XPATH, "//*[contains(@class, 'DivItemContainerV2')]")
                # print(all_videos)
                for i in all_videos:
                    i.click()
                    time.sleep(5)
                    self.driver.find_element(By.XPATH,"//*[contains(@class, 'xgplayer-container')]").click()
                    time.sleep(40)
                    self.driver.implicitly_wait(20)
                    close_video = self.driver.find_element(By.XPATH, "//*[contains(@class, 'StyledCloseIconContainer')]")
                    comments = self.driver.find_elements(By.XPATH, "//*[contains(@class, 'DivCommentContentContainer')]")
                    if comments:
                        # is_author = self.driver.find_element(By.XPATH, "//*[contains(@class, 'SpanIdentity')]")
                        reply_comment = self.driver.find_element(By.XPATH, "//*[contains(@class, 'SpanReplyButton')]")
                        comment_input = self.driver.find_element(By.XPATH, "//*[contains(@class, 'DraftEditorPlaceholder')]")
                        send_comment = self.driver.find_element(By.XPATH, "//*[contains(@class, 'DivPostButton')]")

                        for comment in comments:
                            print(comment.text)
                    else:
                        print("comment yo'q")
                    time.sleep(5)

                    close_video.click()
                    # return
            except NoSuchElementException as er:
                print(er)
            time.sleep(900)




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
    tiktok_bot = TikTokBot(password="your_pass",username="your_username",text="Salom")
    tiktok_bot.get_cookies()
    time.sleep(10)
    tiktok_bot.reply_comment()

if __name__ == "__main__":
    main()
