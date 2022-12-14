# returnstk is a software coded by OjanRN
# github.com/ojanrn

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime as dt
import time
import sys

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

def argdiff():
    global tickerName
    global returnIter
    returnIter = 0
    tickerName = "N/A"
    for args in range(len(sys.argv)):
        if sys.argv[args] == "-s":
            if sys.argv[args + 1].isupper():
                tickerName= sys.argv[args + 1]
                print(f"tickername set to {tickerName}")
                args += 1
            else:
                print("[LOG] Please enter ticker symbol in uppercase")
        if sys.argv[args] == "-p":
            if sys.argv[args + 1].isnumeric():
                returnIter = sys.argv[args + 1]
                print(f"iterate = {returnIter}")
            else:
                print("[LOG] Please enter the period")
    if tickerName == "N/A":
        print("[LOG] please enter a ticker symbol")
        exit()

def main():
    if len(sys.argv) == 1:
        print("[LOG] No keyword arguments detected, please enter an argument")
        exit()
    argdiff()
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
    if int(returnIter) == 0:
        while True:
            try:
                currentPrc = driver.find_element(by="xpath", value="/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[6]/div/div/div/div[3]/div[1]/div/fin-streamer[1]")
                print(f">Current Price:{currentPrc.text}", end="\r")
                time.sleep(0.50)
            except KeyboardInterrupt:
                print(f">Current Price:{currentPrc.text}")
                print("Keyboard Interrupt detected, exiting program...")
                exit()
    else:
        for i in range(int(returnIter)*2):
            try:
                currentPrc = driver.find_element(by="xpath", value="/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[6]/div/div/div/div[3]/div[1]/div/fin-streamer[1]")
                print(f">Current Price:{currentPrc.text}", end="\r")
                time.sleep(0.50)
            except KeyboardInterrupt:
                print(f">Current Price:{currentPrc.text}")
                print("Keyboard Interrupt detected, exiting program...")
                exit()
        print(f">Current Price:{currentPrc.text}")
        print(f"program exited from iterating for {returnIter} seconds")

print(main())