import time
import csv
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from typing import List
from selenium.webdriver.remote.webelement import WebElement


##### Global ######
#Link="https://www.tase.co.il/en/market_data/index/137/components/index_weight"
Link = "https://www.tase.co.il/en/"
###################


def menu():
    while True:
        print(""" Menu :
              1. Quit
              2. Looking for...
              3. Print all 
              4. Reload
              """)
        cmd= input("Please input your choose: " )
        if cmd=="1" : break
        elif cmd=="2": look_f2()
        elif cmd=="3":print_all_f3()
        elif cmd=="4":reload_f4()
        else: print('Wrong input')


def look_f2():
    found = False
    x = 1
    print("Enter an element that you are looking for:\n")
    find = input().upper()
    print(find)
    d: WebDriver = setup_driver()
    correct_page(d)
    for n in range(4):
        for i in range(30):
            list: List[WebElement] = d.find_elements(By.XPATH,
                                                     "//*[@id='mainContent']/index-lobby/index-composition/index-weight/gridview-lib/div/div[2]/div/div/div[2]/table/tbody/tr")


            for l in list:
                element = l.text.split("\n", 1)[0]
                if element == find:
                    print(element)
                    d.find_element(By.XPATH,
                                   f"//*[@id='mainContent']/index-lobby/index-composition/index-weight/gridview-lib/div/div[2]/div/div/div[2]/table/tbody/tr[{x}]/td[1]/a").click()

                    d.find_element(By.XPATH,
                                   "//*[@id='mainContent']/security-lobby/security-major/section[1]/div/div[1]/div/div[2]/chart-period-menu/ul/li[6]/a/span").click()
                    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                    d.save_screenshot(f".\\Screenshots\\{find}_{now}.png")
                    found = True
                    break
                x = x + 1

            if found:
                break
        if found:
            print("found")
            break
        print("-------------------")
        d.find_element(By.XPATH, "//*[@id='pageS']/pagination-template/ul/li[8]/a").click()
        x=1
        time.sleep(2)
    if found == False:
        print("The element has not found")
    close_driver(d)


def print_all_f3():
    row = []
    d: WebDriver = setup_driver()
    correct_page(d)
    for n in range(4):
        for i in range(30):

            list1: List[WebElement] = d.find_elements(By.XPATH,"//*[@id='mainContent']/index-lobby/index-composition/index-weight/gridview-lib/div/div[2]/div/div/div[2]/table/tbody/tr")
            for l in list1:
                if l.text is None:
                    continue
                row.clear()
                line = l.text.split("\n")
                line.pop()
                row.append(line[0])
                row = row + line[-1].split(" ")
                print(row)

        d.find_element(By.XPATH, "//*[@id='pageS']/pagination-template/ul/li[8]/a").click()
        time.sleep(2)
    close_driver(d)



def reload_f4():
    d: WebDriver = setup_driver()
    row=[]
    correct_page(d)
    for n in range(4):
        for i in range(30):
            list: List[WebElement] = d.find_elements(By.XPATH,
                                                     "//*[@id='mainContent']/index-lobby/index-composition/index-weight/gridview-lib/div/div[2]/div/div/div[2]/table/tbody/tr")

            with open("data.csv", 'w', newline='', encoding='UTF8') as file:

                fieldNames = ['Name', 'Symbol',"Security No","ISIN","Weight (%)","Market Cap (NIS millions)","Base Price","Ex"]
                writer = csv.writer(file)
                writer.writerow(fieldNames)

                for l in list:
                   if l.text is None:
                         continue
                   row.clear()
                   line = l.text.split("\n")
                   line.pop()
                   row.append(line[0])
                   row=row+line[-1].split(" ")
                   #print(row)
                   writer.writerow(row)
        d.find_element(By.XPATH, "//*[@id='pageS']/pagination-template/ul/li[8]/a").click()
        time.sleep(2)
    print("Data has been reloaded in the scv file")
    close_driver(d)



def correct_page(driver) -> str:
    print("correct page")
    d : WebDriver=driver
    d.get(Link)
    time.sleep(1)
    driver.find_element(By.XPATH,
                        "//*[@id='trades_panel1']/article/div[1]/top-indices/table/tbody/tr[3]/td[1]/a").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//*[@id='mainContent']/index-lobby/section[1]/div/div/section[2]/button").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//*[@id='more_madad_nav']/ul/li[1]/ul/li[4]/a").click()
    time.sleep(1)
    driver.find_element(By.XPATH,"//*[@id='mainContent']/index-lobby/index-composition/index-weight/gridview-lib/div/div[2]/div/div/div[2]/table/thead/tr[2]/td[6]/ul/li[2]/button").click()
    time.sleep(1)




def setup_driver() -> WebDriver:
    driver: WebDriver = webdriver.Chrome(executable_path="drivers/chromedriver.exe")
    print(" ---start setup_driver")
    driver.maximize_window()
    driver.implicitly_wait(11)
    driver.delete_all_cookies()
    return driver


def close_driver(driver: WebDriver):
    print("--start close_driver")
    driver.close()
    driver.quit()



if __name__ == '__main__':
    menu()
    print('---start main')

   # close_driver(d)



