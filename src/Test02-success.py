from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging

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

    # 设置 logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # 等待页面加载
    time.sleep(2)

    # 找到并点击 "Picking Record"
    picking_record = driver.find_element(By.XPATH, '//a[@href="/picking_record"]')
    picking_record.click()

    # 等待新页面加载
    time.sleep(2)

    # 定位到表格
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//table'))
    )

    rows = driver.find_elements(By.XPATH, '//table//tr')[1:]

    for row_index in range(len(rows)):
        # 每次都重新获取 rows，因为页面刷新后之前的元素已失效
        rows = driver.find_elements(By.XPATH, '//table//tr')[1:]
        row = rows[row_index]

        cols = row.find_elements(By.TAG_NAME, 'td')
        logging.info(f"第 {row_index + 1} 行，共 {len(cols)} 列")

        for col_index in range(1, len(cols)):
            try:
                # 每次点击前都重新获取 col 元素
                rows = driver.find_elements(By.XPATH, '//table//tr')[1:]
                row = rows[row_index]
                cols = row.find_elements(By.TAG_NAME, 'td')
                col = cols[col_index]

                link = col.find_element(By.TAG_NAME, 'a')

                if link:
                    logging.info(f"点击链接：{link.text}")
                    link.click()

                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.TAG_NAME, 'body'))
                    )

                    time.sleep(3)  # 等待查看详情页

                    driver.back()

                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//table'))
                    )

                    time.sleep(2)

            except Exception as e:
                logging.warning(f"第 {row_index + 1} 行第 {col_index + 1} 列点击失败：{e}")
                continue


finally:
    time.sleep(10)  #
    driver.quit()  # 关闭浏览器
