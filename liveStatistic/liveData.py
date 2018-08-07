# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import lsConfig
import logging
import logging.config


SOURCE_CONFIG = lsConfig.config()['SOURCE']
logging.config.fileConfig("logger.conf")


def login(username, passwd, driver):
    sleep(10)
    # Switch to login frame
    driver.switch_to.frame('udbsdk_frm_normal')

    sleep(1)
    # Input username
    acc_input = driver.find_element_by_class_name('E_acct')
    acc_input.send_keys(username)

    sleep(1)
    # Input password
    pwd_input = driver.find_element_by_class_name('E_passwd')
    pwd_input.send_keys(passwd)

    sleep(3)
    # Login Huya
    wait = WebDriverWait(driver, 20)
    login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#m_commonLogin > div.form_item.form_opra > a.m_button_large.E_login')))
    login_button.click()
    sleep(5)


def login_with_cookies(cookies_obj, driver):
    cookies = []
    if(isinstance(cookies_obj, str)):
        cookies = eval(cookies_obj)
    else:
        cookies = cookies_obj

    for cookie in cookies:
        driver.add_cookie(cookie)
    sleep(2)
    driver.get(SOURCE_CONFIG['hy_url'])
    sleep(10)


def init_browser():
    chrome_options = Options()
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.maximize_window()
    driver.get(SOURCE_CONFIG['hy_url'])

    return driver


def get_cookies(driver):
    cookies = []
    cookies_from_browser = driver.get_cookies()

    for item in cookies_from_browser:
        cookies.append({'name': item['name'], 'value':item['value']})

    return cookies


def get_live_data(username, passwd, cookies):
    data_dic = {}

    driver = init_browser()

    if(False):
        login_with_cookies(cookies, driver)
        logging.info("Log in with cookies for user: " + str(username))
    else:
        login(username, passwd, driver)
        logging.info("Log in with acc/pwd for user: " + str(username))
        logging.info("Cookies: " + str(get_cookies(driver)))

    # Go to profile live history tag
    driver.find_element_by_xpath("//a[@menu='profileLiveHistory']").click()

    # Go to 30 day statistics
    driver.find_element(By.CSS_SELECTOR, 'div.live__statistics > ul.tit-tabs > li:nth-child(2)').click()

    # List tags
    for tag in SOURCE_CONFIG['tags']:
        i_tag = "#" + tag
        sleep(5)
        driver.find_element(By.CSS_SELECTOR, i_tag).click()
        name = driver.execute_script("return window.option.series[0].name")
        data = driver.execute_script("return window.option.series[0].data")

        data_dic[name] = data

    sleep(2)
    driver.quit()
    logging.info("Log out user: " + str(username))

    return data_dic

