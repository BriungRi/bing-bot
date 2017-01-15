import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from random import randint
#Don't worry about next 3 lines
import json
with open('userinfo.json') as data_file:
    credentials = json.load(data_file)

def sign_in(browser, email, password):
    time.sleep(1)
    browser.get('https://login.live.com/login.srf?wa=wsignin1.0&rpsnv=13&ct=1481167372&rver=6.7.6631.0&wp=MBI&wreply=https%3a%2f%2fwww.bing.com%2fsecure%2fPassport.aspx%3frequrl%3dhttps%253a%252f%252fwww.bing.com%252frewards%252fsignin%253fwlexpsignin%253d1&lc=1033&id=264960')

    email_text_field = browser.find_element_by_xpath('//*[@id="i0116"]')
    email_text_field.send_keys(email)

    next_button = browser.find_element_by_xpath('//*[@id="idSIButton9"]')
    next_button.click()

    time.sleep(1)

    password_text_field = browser.find_element_by_xpath('//*[@id="i0118"]')
    password_text_field.send_keys(password)

    sign_in_button = browser.find_element_by_xpath('//*[@id="idSIButton9"]')
    sign_in_button.click()

def sign_out(browser):
    browser.get('https://account.microsoft.com/rewards/dashboard')
    browser.find_element_by_xpath('//*[@id="meControl"]').click()
    browser.find_element_by_xpath('//*[@id="msame_si1"]/a').click()

def search(browser, phrase):
    browser.get('http://www.bing.com/')
    time.sleep(randint(3, 6))
    search_text_field = browser.find_element_by_xpath('//*[@id="sb_form_q"]')
    search_text_field.clear()
    search_text_field.send_keys(phrase)

    search_text_field.send_keys(Keys.RETURN)

def get_points(browser):
    browser.get('https://account.microsoft.com/rewards/dashboard')
    time.sleep(1)
    title = browser.find_element_by_xpath('//*[@id="dashboard"]/div[2]/div[3]/div[4]/div/div[1]/a').text
    num_points = None
    if title == "PC search":
        num_points = int(browser.find_element_by_xpath('//*[@id="dashboard"]/div[2]/div[3]/div[4]/div/div[3]').text.replace(' of 150 points', ''))
    else:
        num_points = int(browser.find_element_by_xpath('//*[@id="dashboard"]/div[2]/div[3]/div[5]/div/div[3]').text.replace(' of 150 points', ''))
    print(num_points)
    return num_points

# Main code starts here
browser = webdriver.Chrome('/usr/local/bin/chromedriver')

logins = open('real_logins.txt', 'r').read().split('\n')
words = open('words.txt', 'r').read().split('\n')
for login in logins:
    info = login.split(':')
    sign_in(browser, info[0], info[1])
    points = get_points(browser)
    while points < 150:
        for i in range(randint(3, 6)):
            search(browser, words[randint(0, len(words) - 1)])
        points = get_points(browser)
    sign_out(browser)
