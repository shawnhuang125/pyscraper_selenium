import os
import json
import time
import random
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def google_search_selenium(query, num_results=10):
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")  
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get("https://www.google.com/")
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)

    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.MjjYud")))

    results = []
    search_results = driver.find_elements(By.CSS_SELECTOR, "div.MjjYud")[:num_results]
    #逐筆擷取 Google 搜尋結果的標題、網址與摘要，然後放進 results 清單
    for result in search_results:
        #使用try可以防止抓不到元素時整個程式中斷
        try:
            #找出 result 裡面的 h3 元素，這個是是搜尋結果的標題元素,執行 .text 抓取該元素的文字
            title = result.find_element(By.CSS_SELECTOR, "h3").text
            #找出該搜尋結果中第一個 <a>（超連結）標籤,取得該連結的網址
            link = result.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            #如果有找到 div.VwiC3b（這個是摘要文字的容器），就執行 .text 抓文字
            #如果沒有這個元素，就給一個預設字串 "無摘要"
            snippet = result.find_element(By.CSS_SELECTOR, "div.VwiC3b").text if result.find_elements(By.CSS_SELECTOR, "div.VwiC3b") else "無摘要"
            #把抓到的資料組成字典，共有三個欄位：標題,網址及摘要
            results.append({"標題": title, "網址": link, "摘要": snippet})
        except Exception as e:
            #如果有任何一行出現錯誤，就會進入這裡
            #會列印出錯誤原因，不會中斷程式執行
            print(f"錯誤: {e}")

    driver.quit()
    return results
    #儲存檔案
def save_results(results, query):
    # 自訂儲存資料夾名稱
    save_dir = "./data"

    # 如果資料夾不存在，就建立並提示；否則顯示已存在
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        print(f"資料夾已建立：{save_dir}")
    else:
        print(f"資料夾已存在：{save_dir}")

    #使用時間序命名避免檔案混淆
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    
    json_filename = os.path.join(save_dir, f"{query.replace(' ', '_')}_{timestamp}.json")
    md_filename = os.path.join(save_dir, f"{query.replace(' ', '_')}_{timestamp}.md")
    txt_filename = os.path.join(save_dir, f"{query.replace(' ','_')}_{timestamp}.txt")

    #寫入並儲存成JSON檔案(.json)
    #讓中文等非 ASCII 字元可以正常儲存,縮排 4 個空格
    with open(json_filename, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

    #寫入並儲存成Markdown(.md)
    with open(md_filename, "w", encoding="utf-8") as f:
        f.write(f"# Google 搜尋結果: {query}\n\n")
        #寫入 Markdown 標題，用 # 表示一級標題
        for i, result in enumerate(results, start=1):
            #寫入markdown的超連結
            f.write(f"### {i}. [{result['標題']}]({result['網址']})\n\n")
            #寫入網的摘要
            f.write(f"> {result['摘要']}\n\n")
            #寫入一條分隔線 ---
            f.write("---\n\n") 
    #寫入並儲存成txt(.txt)
    with open(txt_filename, "w", encoding="utf-8") as f:
        f.write(f"Google 搜尋結果: {query}\n\n")
        #寫入標題與搜尋關鍵字
        for i, result in enumerate(results, start=1):
            #寫入標題
            f.write(f"{i}. {result['標題']}\n")
            #寫入網址
            f.write(f"   網址: {result['網址']}\n")
            #寫入摘要並換行
            f.write(f"   摘要: {result['摘要']}\n\n")

    #列出三個輸出檔案的路徑與檔名,可以方便查找
    print(f"\n搜尋結果已儲存：")
    print(f"- JSON 檔案: {json_filename}")
    print(f"- Markdown 檔案: {md_filename}")
    print(f"- 純文字檔案: {txt_filename}")

query = input("請輸入 Google 搜尋關鍵字: ")

results = google_search_selenium(query)

if results:
    save_results(results, query)

    print("\n=== 搜尋結果 ===\n")
    for i, result in enumerate(results):
        print(f"{i+1}. [{result['標題']}]({result['網址']})")
        print(f"   {result['摘要']}\n")
else:
    print("沒有找到任何結果。")
