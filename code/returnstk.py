# returnstk is a software coded by OjanRN
# github.com/ojanrn

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime as dt
import time

def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument("no-sandbox")
    options.add_argument("disable-dev-shm-usage")
    options.add_argument("log-level=3")
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(options=options)
    driver.get("https://finance.yahoo.com")
    return driver

def simType(element,text):
    for char in text:
        element.send_keys(char)
        time.sleep(0.05)

def main():
    tickerName = input("Ticker Symbol? ")
    print("")
    driver = get_driver()
    time.sleep(0.5)
    searchBar = driver.find_element(by="id", value="yfin-usr-qry")
    marketStatus = driver.find_element(by="xpath", value="/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[4]/div/div/div/div[1]/div/div/span")
    print(f"[LOG]: {marketStatus.text} > {dt.now().strftime('%H-%M-%S')}")
    print(f"[LOG]: searching ticker > {dt.now().strftime('%H-%M-%S')}")
    simType(searchBar, tickerName)
    time.sleep(1)
    print(f"[LOG]: accessing stock page > {dt.now().strftime('%H-%M-%S')}")
    driver.find_element(by="id", value="result-quotes-0").click()
    print(f"[LOG]: getting price information > {dt.now().strftime('%H-%M-%S')}")
    company = driver.find_element(by="xpath", value="/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[6]/div/div/div/div[2]/div[1]/div[1]/h1")
    print(f"[LOG]: showing information for: {company.text}")
    time.sleep(2)
    try:
        blockmsg = driver.find_element(by="xpath", value="/html/body/div[1]/div/div/div[1]/div/div[4]/div/div/div[1]/div/div/div/div/div/section/button[1]")
        blockmsg.click()
    except:
        pass
    time.sleep(1)
    print("")
    while True:
        try:
            currentPrc = driver.find_element(by="xpath", value="/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[6]/div/div/div/div[3]/div[1]/div/fin-streamer[1]")
            print(f">Current Price:{currentPrc.text}", end="\r")
            time.sleep(0.25)
        except KeyboardInterrupt:
            print("Keyboard Interrupt detected, exiting program...")

print(main())