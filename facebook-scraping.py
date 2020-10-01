

import requests
from secrets import username, password

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import csv
import json

'''
 * check if the comment contains more than 80% bangla text
 * reduce newlines
 * 50% positive, 50% negative comment
'''


class FacebookBot():
    
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-notifications')
        self.driver = webdriver.Chrome(options=options)
        
    def login(self, username, password):
        self.driver.get("https://www.facebook.com/login")
        
        sleep(2)
        
        email_in = self.driver.find_element_by_xpath('//*[@id="email"]')
        email_in.send_keys(username)
        
        password_in = self.driver.find_element_by_xpath('//*[@id="pass"]')
        password_in.send_keys(password)
        
        login_btn = self.driver.find_element_by_xpath('//*[@id="loginbutton"]')
        login_btn.click()
        
        sleep(2)
    
    
    # go to the post via mbasic.facebook.com
    # paste the post url
    def get_comments (self, url):
        self.driver.get(url)
        
        #click more
        while True:
            try:
                loadMoreButton = self.driver.find_element_by_xpath('//*[@class="_108_"]')
                time.sleep(1)
                loadMoreButton.click()
                time.sleep(1)
            except Exception as e:
                break
        
        names = []
        links = self.driver.find_elements_by_tag_name('div')
        for link in links:
            if link.get_attribute('class') == '_2b05':
                names.append(link.text)
        
        comments = []
        links = self.driver.find_elements_by_tag_name('div')
        for link in links:
            if link.get_attribute('data-sigil') is not None and link.get_attribute('data-sigil') == 'comment-body':
                comments.append(link.text)
                
        new = FacebookBot()
        new.login(username, password)
                
        reacts = []
        links = self.driver.find_elements_by_tag_name('a')
        for link in links:
            if link.get_attribute('class') == '_14v8 _4edm':
                new.driver.get(link.get_attribute('href'))
                react = [0]*8
                tags = new.driver.find_elements_by_tag_name('span')
                for tag in tags:
                    if tag.get_attribute('data-sigil') is not None and tag.get_attribute('data-sigil') == 'reaction_profile_sigil':
                        if json.loads(tag.get_attribute('data-store'))['reactionType'] == 'all':
                            react[0] = tag.text[4:]
                        elif json.loads(tag.get_attribute('data-store'))['reactionType'] == 1:
                            react[1] = tag.text
                        elif json.loads(tag.get_attribute('data-store'))['reactionType'] == 2:
                            react[2] = tag.text
                        elif json.loads(tag.get_attribute('data-store'))['reactionType'] == 16:
                            react[3] = tag.text
                        elif json.loads(tag.get_attribute('data-store'))['reactionType'] == 4:
                            react[4] = tag.text
                        elif json.loads(tag.get_attribute('data-store'))['reactionType'] == 3:
                            react[5] = tag.text
                        elif json.loads(tag.get_attribute('data-store'))['reactionType'] == 7:
                            react[6] = tag.text
                        elif json.loads(tag.get_attribute('data-store'))['reactionType'] == 8:
                            react[7] = tag.text
                reacts.append(tuple(react))
            elif link.get_attribute('class') == '_14v8':
                reacts.append(tuple([0]*8))
        
        new.driver.close()
        
        with open('comments.csv', 'w', newline='', encoding="utf-32") as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Comment", "Reacts", "Like", "Love", "Care", "Haha", "Wow", "Sad", "Angry"])
            for (name, comment, react) in zip(names, comments, reacts):
                t = (name, comment) + react
                writer.writerow(t)
        
        self.driver.close()



if __name__ == '__main__':
    bot = FacebookBot()
    bot.login(username, password)

    print('Please insert the destination url (use mobile version m.facebook.com)')
    url = input('> ')
    
    bot.get_comments(url)
    
    print('Task executed successfully!')
