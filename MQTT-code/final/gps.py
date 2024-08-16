from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import paho.mqtt.client as mqtt
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

# Setting Chrome Browser
chrome_options = Options()
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--allow-geolocation")
#chrome_options.add_argument("--headless")

# ChromeDriver dir
service = Service('/home/whyhugo/Documents/Smart Cities/Data-Science-Communication-course/MQTT-code/chromedriver-linux64/chromedriver')

# Initialize WebDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

def get_coordinates():
    try:
        # The website we can get coordinates
        driver.get("https://gps-coordinates.org/")
        driver.minimize_window()

        time.sleep(5)

        # Get latitude and longitude
        latitude = driver.find_element(By.ID, "latitude").get_attribute("value")
        longitude = driver.find_element(By.ID, "longitude").get_attribute("value")

        print(f"Your current coordinates is Latitude: {latitude}, Longitude: {longitude}")
        return latitude, longitude

    finally:
        driver.quit()

# Function to select the emergency type
def select_emergency_type():
    print("Select the emergency type:")
    print("1. Fire")
    print("2. Medical Emergency")
    print("3. Security Threat")
    print("4. Technical Failure")
    print("5. Other")

    choice = input("Enter the number corresponding to the emergency type: ")

    emergency_types = {
        "1": "Fire",
        "2": "Medical Emergency",
        "3": "Security Threat",
        "4": "Technical Failure",
        "5": "Other"
    }

    return emergency_types.get(choice, "Other")

# MQTT settings
MQTT_BROKER = "140.122.185.98"
MQTT_PORT = 1883
MQTT_TOPIC = "gps/location"

# MQTT on_connect callback
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc))

# MQTT on_publish callback
def on_publish(client, userdata, mid):
    print("Message Published...")

# Main function to publish GPS location and emergency type
def publish_location():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.username_pw_set(config['NTNUpw']['username'], config['NTNUpw']['password'])
    client.connect(MQTT_BROKER, MQTT_PORT, 60)

    # Retrieve GPS coordinates using Selenium
    latitude, longitude = get_coordinates()

    # Select the emergency type
    emergency_type = select_emergency_type()

    if latitude and longitude:
        gps_data = f"📍latitude: {latitude}, longitude: {longitude}, 📢 Emergency_type: {emergency_type}"
        # Convert dictionary to string for publishing
        gps_payload = f"{gps_data}"

        # Publish to MQTT broker
        client.publish(MQTT_TOPIC, gps_payload)

        print(f"❗️Emergency Alert: {gps_payload}")
    else:
        print("Unable to get GPS location")

    client.disconnect()

if __name__ == "__main__":
    publish_location()
