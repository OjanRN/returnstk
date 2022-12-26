# returnstk is a software coded by OjanRN
# github.com/ojanrn

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime as dt
import time
import keyboard
import sys

welcomeText = """
           _                        _   _    
  _ __ ___| |_ _   _ _ __ _ __  ___| |_| | __
 | '__/ _ \ __| | | | '__| '_ \/ __| __| |/ /
 | | |  __/ |_| |_| | |  | | | \__ \ |_|   < 
 |_|  \___|\__|\__,_|_|  |_| |_|___/\__|_|\_\                                              
"""

helpText = '''
+-----+----------+-----------------+------------------+
|FLAG | SYNONYM  | DESCRIPTION     | DEFAULT VALUE    |
|-h   | --help   | Help            |                  |
|-s   | --symbol | Ticker Symbol   | Unknown          |
|-p   | --period | Period(Seconds) | 0(Infinite)      |
|-sv  | --save   | Save File       | 0(Not Saved)     |
+-----+----------+-----------------+------------------+
|                                                     |
|Example usage: <executable> -h, <executable> -s **** |
+-----------------------------------------------------+
'''

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

def createf():
    filename = f"{dt.now().strftime('%Y-%m-%d-%H')}.txt"
    with open(filename, 'w') as file:
        file.write(f"DATA RECORDED AT: {dt.now().strftime('%Y-%m-%d-%H-%M-%S')}\n")
        file.close()

def writeln(text):
    filename = f"{dt.now().strftime('%Y-%m-%d-%H')}.txt"
    with open(filename, 'a') as file:
        file.write(text)
        file.close()        

def argdiff():
    global tickerName
    global returnIter
    global saveOpt
    saveOpt = 0
    returnIter = 0
    tickerName = "N/A"
    for args in range(len(sys.argv)):
        if sys.argv[args] in ["-s", "--symbol"]:
            if sys.argv[args + 1].isupper():
                tickerName= sys.argv[args + 1]
                args += 1
            else:
                print("[LOG] Please enter ticker symbol in uppercase")
        if sys.argv[args] in ["-p","--period"]:
            if sys.argv[args + 1].isnumeric():
                returnIter = sys.argv[args + 1]
                print(f"iterate = {returnIter}")
            else:
                print("[LOG] Please enter the period")
        if sys.argv[args] in ["-sv","--save"]:
            if int(sys.argv[args + 1]) < 2:
                saveOpt = sys.argv[args + 1]
            else:
                print("Please enter a valid save option: 0 or 1")
            print("h")
        if sys.argv[args] in ["-h","--help"]:
            print(helpText)
            exit()
    if tickerName == "N/A":
        print("[LOG] please enter a ticker symbol")
        exit()

def priceStreamer():
    if int(returnIter) == 0:
        while True:
            currentPrc = driver.find_element(by="xpath", value="/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[6]/div/div/div/div[3]/div[1]/div/fin-streamer[1]")
            print(f">Current Price:{currentPrc.text}", end="\r")
            time.sleep(0.50)
            if keyboard.is_pressed("e"):
                print(f">Current Price:{currentPrc.text}")
                print("Keyboard Interrupt detected, exiting program...")
                exit()
    else:
        for i in range(int(returnIter)*2):
            currentPrc = driver.find_element(by="xpath", value="/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[6]/div/div/div/div[3]/div[1]/div/fin-streamer[1]")
            print(f">Current Price:{currentPrc.text}", end="\r")
            time.sleep(0.50)
            if keyboard.is_pressed("e"):
                print(f">Current Price:{currentPrc.text}")
                print("Keyboard Interrupt detected, exiting program...")
                exit()
        print(f">Current Price:{currentPrc.text}")
        print(f"program exited from iterating for {returnIter} seconds")
        exit()

def main():
    if len(sys.argv) == 1:
        print("[LOG] No keyword arguments detected, please enter an argument")
        exit()
    argdiff()
    global driver
    global company 
    print(welcomeText)
    print(f"[LOG] starting returnstk at {dt.now().strftime('%H-%M-%S')}")
    driver = get_driver()
    time.sleep(0.5)
    try:
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
    except:
        print(f"[LOG] error occured > {dt.now().strftime('%H-%M-%S')}")
    print(f"[LOG]: showing information for: {company.text}")
    time.sleep(2)
    try:
        blockmsg = driver.find_element(by="xpath", value="/html/body/div[1]/div/div/div[1]/div/div[4]/div/div/div[1]/div/div/div/div/div/section/button[1]")
        blockmsg.click()
    except:
        pass
    time.sleep(1)
    print("")
    if saveOpt == "1":
        createf()
        if int(returnIter) == 0:
            while True:
                currentPrc = driver.find_element(by="xpath", value="/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[6]/div/div/div/div[3]/div[1]/div/fin-streamer[1]")
                print(f">Current Price:{currentPrc.text}", end="\r")
                writeln(f"{currentPrc.text} > {dt.now().strftime('%H-%M-%S')}\n")
                time.sleep(0.50)
                if keyboard.is_pressed("e"):
                    print(f">Current Price:{currentPrc.text}")
                    print("Keyboard Interrupt detected, exiting program...")
                    exit()
        else:
            for i in range(int(returnIter)*2):
                currentPrc = driver.find_element(by="xpath", value="/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[6]/div/div/div/div[3]/div[1]/div/fin-streamer[1]")
                print(f">Current Price:{currentPrc.text}", end="\r")
                writeln(f"{currentPrc.text} > {dt.now().strftime('%H-%M-%S')}\n")
                time.sleep(0.50)
                if keyboard.is_pressed("e"):
                    print(f">Current Price:{currentPrc.text}")
                    print("Keyboard Interrupt detected, exiting program...")
                    exit()
            print(f">Current Price:{currentPrc.text}")
            print(f"program exited from iterating for {returnIter} seconds")
            exit()
    else:
        priceStreamer()

print(main())