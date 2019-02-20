from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import sys


class InstaDownload:
    # initializes the browser and driver
    browser = webdriver.Chrome("/your/path/to/chromedriver")

    # empty list where the links are stored
    links = []

    # stores the urls
    urls = []

    # stores the usernames to be printed when finalized
    usernames = []

    # list any desired hastags
    hashtags = ["any", "valid", "hastags", "go", "here", "do", "not", "include", "the", "#"
                ]
###################################################################################################

    def __init__(self):
        self.get_top()
        self.get_usernames()
        try:
            self.download()
        finally:
            self.end()

    # gets the usernames
    def get_top(self):
            for hashtag in self.hashtags:

                self.browser.get('https://www.instagram.com/explore/tags/' + hashtag + '/')
                time.sleep(2)

                links = self.browser.find_elements_by_tag_name('a')
                condition = lambda link: '/p/' in link.get_attribute('href')
                valid_links = list(filter(condition, links))

                # change the range to download more or less than the top 9 posts
                for i in range(0, 9):
                    link = valid_links[i].get_attribute('href')
                    if link not in self.links:
                        self.links.append(link)

    # goes through the links and obtains the usernames of each picture
    def get_usernames(self):
        for link in self.links:
            self.browser.get(link)
            the_element = self.browser.find_element_by_xpath("//a[@class='FPmhX notranslate nJAzx']")
            go = the_element.get_attribute("title")
            self.usernames.append(go)

    # goes to instadownload.com and downloads the pictures
    def download(self):
        self.browser.get('https://downloadgram.com/')
        time.sleep(5)

        # switches out of an iframe commonly seen on the website
        element = self.browser.find_element_by_xpath(
            "//div[starts-with(@id,'id')]" and """//div[starts-with(@style,'position:absolute !important;height:20px 
            !important;width:20px !important;top:3px !important;left:3px !important;background-image:url(data:image/png;
            ')]""")
        if element:
            self.browser.execute_script("arguments[0].click();", element)
            time.sleep(1)

        # inputs and downloads
        for link in self.links:
            try:
                input = self.browser.find_element_by_xpath('//input[@name="url"]')
                input.clear()
                input.send_keys(link)
                time.sleep(1)

                download = self.browser.find_element_by_xpath("//input[@type='submit']")
                download.click()
                time.sleep(3)

                try:
                    WebDriverWait(self.browser, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//a[@target='_blank']"))
                    )
                except TimeoutException:
                    print(
                        "Timed out waiting for page to load")
                actually_download = self.browser.find_element_by_xpath("//a[@target='_blank']")
                actually_download.click()
                time.sleep(2)
            except ValueError:
                print("link broke")

    # terminates and prints usernames
    def end(self):
        num = 1
        for username in self.usernames:
            print(username + ' ' + str(num) + ', ')
            num += 1
        self.browser.close()
        sys.exit()


InstaDownload()