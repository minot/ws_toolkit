# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

HY_URL = "https://i.huya.com/"

TAGS = ('iDuration', 'iPeakViewer', 'iGiftCount', 'iNewFans', 'iLiveShare')


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

def initBrower():
    chrome_options = Options()
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.maximize_window()
    driver.get(HY_URL)

    return driver

def getLiveData(username, passwd):
    dataDic = {}

    driver = initBrower()
    login(username, passwd, driver)

    # Go to profile live history tag
    driver.find_element_by_xpath("//a[@menu='profileLiveHistory']").click()

    sleep(5)
    # Go to 30 day statistics
    driver.find_element(By.CSS_SELECTOR, 'div.live__statistics > ul.tit-tabs > li:nth-child(2)').click()

    # List tags
    for tag in TAGS:
        i_tag = "#" + tag
        sleep(5)
        driver.find_element(By.CSS_SELECTOR, i_tag).click()
        name = driver.execute_script("return window.option.series[0].name")
        data = driver.execute_script("return window.option.series[0].data")

        dataDic[name] = data

    return dataDic

