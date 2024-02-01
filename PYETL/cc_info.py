from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time
import csv
def scroll(driver, url):

    driver.get(url)
    driver.execute_script(f"window.scrollBy(0, 5000);")
    times = 0
    while True:
        
    
        # 滾動頁面像素
        scroll_increment = 1
        driver.execute_script(f"window.scrollBy(0, {scroll_increment});")
        
        # 設定滾動次數
        if times == 110000:
            break  
        else:
            
            times += 1
            continue  
def get_iCard(driver, url):

    try:
        
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        all_cards = []

        for cards_element in soup.find_all("div", class_="sc-fkouio-0 jdQMAt"):
            #卡名
            cname_element = cards_element.find("div", class_="sc-fkouio-0 kMjtwV")
            cname = cname_element.text.strip() if cname_element else "Null"
            #國內一般消費利率
            crate_element = cards_element.find("span", class_="sc-fkouio-1 hZqKPi")
            domestic_element = cards_element.find("div", class_="sc-fkouio-0 sc-9y76ir-3 kWEJLk bnqdgJ")
            crate = None
            if domestic_element and domestic_element.text.strip() == "(國內一般消費)":
                rate_text = crate_element.text.strip() if crate_element else ""
                try:
                    crate = float(rate_text)
                except ValueError:
                    crate = None
                # crate = float(rate_text) if rate_text.isdigit() else None
            cissuer_element = cards_element.find("div", class_="sc-fkouio-0 jsbhSP")
            cissuer = cissuer_element.text.strip() if cissuer_element else "Null"
            all_cards.append({"cards": cname, "domestic_rate": crate, "card_issuer": cissuer, "url": None})

        return all_cards
    except TimeoutException:
        print("等待元素時間過長。")
        return []
    except Exception as e:
        print(f"抓取過程出現問題：{e}")
        return []
    finally:
        print("MISSION COMPLETE!!")
# 下面是使用Chrome WebDriver的方式
options = webdriver.ChromeOptions()
options.add_argument('User-Agent = Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

driver = webdriver.Chrome(options=options)

url = "https://icard.ai/home/all_cards" 
driver.get(url)
scroll(driver, url)
#等待頁面加載完成
time.sleep(5)

#爬取資訊
products = get_iCard(driver, url)

#等待爬取時間
time.sleep(5)

#打印資料
with open('cc_info.txt', 'w', encoding='utf-8') as file:
   
    for product in products:
        file.write(f"{product}\n")
        
  
#關閉網頁
driver.quit()


