from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import paho.mqtt.client as mqtt
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

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

def get_coordinates():
    try:
        # 造訪目標網站
        driver.get("https://gps-coordinates.org/")

        # 暫停以等待網站允許位置存取
        time.sleep(5)

        # 獲取緯度和經度
        latitude = driver.find_element(By.ID, "latitude").get_attribute("value")
        longitude = driver.find_element(By.ID, "longitude").get_attribute("value")

        print(f"Latitude: {latitude}, Longitude: {longitude}")
        return latitude, longitude

    finally:
        # 關閉瀏覽器
        driver.quit()

# MQTT settings
MQTT_BROKER = "140.122.185.98"  # Use your MQTT broker's address
MQTT_PORT = 1883
MQTT_TOPIC = "gps/location"

# MQTT on_connect callback
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc))

# MQTT on_publish callback
def on_publish(client, userdata, mid):
    print("Message Published...")

# Main function to publish GPS location
def publish_location():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.username_pw_set(config['NTNUpw']['username'], config['NTNUpw']['password'])
    client.connect(MQTT_BROKER, MQTT_PORT, 60)

    # Retrieve GPS coordinates using Selenium
    latitude, longitude = get_coordinates()

    if latitude and longitude:
        gps_data = {"latitude": latitude, "longitude": longitude}
        # Convert dictionary to string for publishing
        gps_payload = f"{gps_data}"

        # Publish to MQTT broker
        client.publish(MQTT_TOPIC, gps_payload)

        print(f"Published GPS data: {gps_payload}")
    else:
        print("Unable to get GPS location")

    client.disconnect()

if __name__ == "__main__":
    publish_location()
