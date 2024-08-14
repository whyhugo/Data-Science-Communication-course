from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# 設定 Chrome 瀏覽器的選項
chrome_options = Options()
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--allow-geolocation")

# 指定 ChromeDriver 的路徑
service = Service('/home/whyhugo/Documents/Smart Cities/MQTT-code/chromedriver-linux64/chromedriver')

# 初始化 WebDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # 造訪目標網站
    driver.get("https://gps-coordinates.org/")

    # 暫停以等待網站允許位置存取
    time.sleep(5)

    # 獲取緯度和經度
    latitude = driver.find_element(By.ID, "latitude").get_attribute("value")
    longitude = driver.find_element(By.ID, "longitude").get_attribute("value")

    print(f"Latitude: {latitude}, Longitude: {longitude}")

finally:
    # 關閉瀏覽器
    driver.quit()
