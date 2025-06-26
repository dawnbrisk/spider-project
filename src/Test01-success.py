from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time

# 使用 webdriver_manager 自动获取 chromedriver 的路径
service = Service(ChromeDriverManager().install())

# 初始化 WebDriver
driver = webdriver.Chrome(service=service)

# 打开目标网址
url = 'http://8.209.118.176:3000/'
driver.get(url)

# 等待页面加载
time.sleep(2)

try:
    # 找到并点击 "Location Management"
    location_management = driver.find_element(By.XPATH, '//span[contains(text(), "Location Management")]')
    ActionChains(driver).move_to_element(location_management).click().perform()

    # 等待页面加载
    time.sleep(2)

    # 找到并点击 "Picking Record"
    picking_record = driver.find_element(By.XPATH, '//a[@href="/picking_record"]')
    picking_record.click()

    # 等待新页面加载
    time.sleep(2)

    # 你可以在这里进一步处理爬取的数据

finally:
    input("Press Enter to close the browser...")  # 使脚本暂停，直到手动按下 Enter
