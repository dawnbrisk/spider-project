import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 启动 WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# 打开网页
url = 'https://cas.gigacloudtech.com/home'
driver.get(url)

# 显式等待初始化
wait = WebDriverWait(driver, 10)

try:
    # 第一步：点击 "德国仓储系统（WMSDE）"
    location_management = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "德国仓储系统（WMSDE）")]'))
    )
    ActionChains(driver).move_to_element(location_management).click().perform()
    logging.info("点击 '德国仓储系统（WMSDE）' 成功")

    # 第二步：点击 "发货中心"
    shipment_center = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "发货中心")]'))
    )
    ActionChains(driver).move_to_element(shipment_center).click().perform()
    logging.info("点击 '发货中心' 成功")

    # 第三步：点击 "出库进度概览"
    outbound_overview = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "出库进度概览")]'))
    )
    ActionChains(driver).move_to_element(outbound_overview).click().perform()
    logging.info("点击 '出库进度概览' 成功")

    # 第四步：点击 "搜索" 按钮（假设按钮文本是“搜索”）
    search_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "搜索")]'))
    )
    search_button.click()
    logging.info("点击 '搜索' 按钮成功")

except TimeoutException:
    logging.error("某个元素加载超时。")
except NoSuchElementException:
    logging.error("某个元素未找到。")
except Exception as e:
    logging.error(f"出现未知错误: {e}")
