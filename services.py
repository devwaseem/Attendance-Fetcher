# Author: Waseem Akram

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import json
from config import failureKey,URL
import keys as KEYS
import error_codes as ERROR


def __getWebDriver():
    driver = webdriver.PhantomJS(executable_path="./driver/phantomjs")
    driver.set_window_size(1920, 1080)
    return driver

def isLoaded(driver,xpath):
    timeout = 10
    try:
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
        return True
    except TimeoutException:
        return False


def checklogin(username,password,service=False):
    driver = __getWebDriver()
    driver.get(URL)
    try:
        usernamefield = driver.find_element_by_xpath(KEYS.USERNAME_FIELD)
        passwordfield = driver.find_element_by_xpath(KEYS.PASSWORD_FIELD)
        loginButton = driver.find_element_by_class_name(KEYS.LOGIN_BUTTON)
    except:
        if not service:
            return False
        else:
            return driver, False
    usernamefield.clear()
    passwordfield.clear()
    usernamefield.send_keys(username)
    passwordfield.send_keys(password)
    loginButton.click()
    redirected_url = str(driver.current_url).lower()
    if not service:
        return failureKey not in redirected_url
    else:
        return driver, failureKey not in redirected_url

def fetchAttendance(username,password):
    timeouterror = lambda : json.dumps({"status":False,"message":"Timeout waiting for Data","code":ERROR.TIMEOUT,"data":None})
    driver , loggedIn = checklogin(username,password,True)
    if not loggedIn: json.dumps({"status":False,"message":"Credentials Incorrect","data":None,"code":ERROR.CREDENTIALS})
    if not isLoaded(driver,'//span[@data-id="academics"]'): return timeouterror()
    driver.find_element_by_xpath('//span[@data-id="academics"]').click()
    if not isLoaded(driver,'//*[@id="tab_academics"]/div[2]/div/div/a'): return timeouterror()
    driver.find_element_by_xpath('//*[@id="tab_academics"]/div[2]/div/div/a').click()
    try:
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it(driver.find_element_by_xpath('//iframe[@class="contentbox_ql"]')))
    except TimeoutException:
        return timeouterror()
    isLoaded(driver,'//*[@id="attendenceProto_containerForTable"]')
    soup = BeautifulSoup(
        driver.find_element_by_xpath('//*[@id="attendenceProto_containerForTable"]').get_attribute("innerHTML"),
        'html.parser')
    table = soup.findAll("h3", {"class": "ui-accordion-header ui-state-default ui-corner-all ui-accordion-icons"})
    attendencejson = {}
    attendencejson["size"] = len(table)
    attendencejson["data"]=[]
    for t in table:
        tr = t.find("tr")
        tdlist = tr.findAll("td")
        attendencejson["data"].append({
            "course": tdlist[1].text.strip(),
            "total": tdlist[2].text.strip(),
            "present": tdlist[3].text.strip(),
            "absent": tdlist[4].text.strip(),
            "percentage": tdlist[5].text.strip(),
        })
    return json.dumps({"status":True,"message":"Attendance Extraction successful","data":attendencejson,"code":None})