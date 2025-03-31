# Google 搜尋自動化工具（Selenium 版）

## 主要功能

這是一個使用 Python + Selenium 撰寫的 Google 搜尋自動化程式，能夠自動進行關鍵字搜尋並擷取前幾筆結果，包含：

- 網頁標題
- 網址連結
- 摘要文字（若有）

並將搜尋結果儲存成以下三種格式的檔案：

1. `.json`：原始結構化資料
2. `.md`（Markdown）：方便閱讀與匯入筆記工具
3. `.txt`：純文字檔案，適合快速瀏覽或後續處理

## 使用方式

### 環境準備

1. 請在`reqiurements.txt`添加以下套件
```
selenium
webdriver-manager
```
2. 至以下連結下載對應瀏覽器版本的`google-chromedriver`。google chrome版本號可至google瀏覽器的`設定`->`關於chrome`中看到
- 看到以下版本號,基本上對應至第三個點前面的本版號就可以了
```
Chrome is up to date
Version 134.0.6998.178 (Official Build) (64-bit)
```
- [下載連結](https://googlechromelabs.github.io/chrome-for-testing/#stable)
3. 解壓縮後,將`chromedriver.exe`剪下貼至`windows`的根目錄中的自己新增的folder,並命名為`chromedriver`
4. 進入「進階系統設定」→ 環境變數,在「系統變數」中選擇 Path → 編輯 → 新增以下路徑
```
C:\chromedriver\
```
5. 按下`win`+`r`,輸入`cmd.exe`,並輸入以下確認系統已偵測到`chromedriver`成功的話會顯示版本號
- 5-1. 輸入以下指令
```
chromedriver --version
```
- 5-2. 如果安裝正確並有設定環境變數，會看到像這樣的輸出
```
ChromeDriver 120.0.6099.71 (some-hash)
```
6. 安裝`python`套件
```
pip install -r requirement.txt
```
- 或將文件內容貼到你自己的`reqiurements.txt`
- 在執行一次
```
pip install -r requirement.txt
```
7. 可手動輸入搜尋關鍵字測試使否正常運行

8. 安裝git
```
sudo apt update         # Debian/Ubuntu 系
sudo apt install git

# 或 CentOS/Rocky Linux
sudo yum install git
```
9. Clone GitHub 專案
```
git clone https://github.com/shawnhuang125/pyscraper_selenium.git
cd pyscraper_selenium
```
10. 建立虛擬環境（建議）
```
python3 -m venv venv
source venv/bin/activate
```
11. 執行專案
```
python search.py
```
- 或是整合進你的專案,再透過你的應用運行
