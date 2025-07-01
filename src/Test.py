import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.action_chains import ActionChains

from webdriver_manager.chrome import ChromeDriverManager
import time

import psutil
import requests



# ========== 初始化 WebDriver ==========
options = Options()

# ① Headless 模式（节省内存 + 隐藏界面）

options.add_argument('--disable-gpu')  # Headless 时必须（Windows 特别需要）
options.add_argument('--window-size=1920,1080')  # 避免无头模式下页面加载异常

# ② 反爬虫设置（防止 navigator.webdriver 被检测）
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

# ③ 可选优化（节省更多资源）
options.add_argument('--blink-settings=imagesEnabled=false')  # 不加载图片

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": "Object.defineProperty(navigator, 'webdriver', { get: () => undefined })"
})

# 获取当前主进程（ChromeDriver）和其子进程（Chrome）
driver_pid = driver.service.process.pid
chrome_driver_process = psutil.Process(driver_pid)

wait = WebDriverWait(driver, 15)
actions = ActionChains(driver)


# ========== 登录并处理滑块 ==========
def login():
    driver.get("https://www.gigab2b.com/index.php?route=account/login")

    email_input = wait.until(EC.visibility_of_element_located(
        (By.XPATH, '//input[@placeholder="Email"]')
    ))
    email_input.send_keys("demo@buyer.com")

    password_input = wait.until(EC.visibility_of_element_located(
        (By.XPATH, '//input[@placeholder="Password"]')
    ))
    password_input.send_keys("!u67q12dM")

    login_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//button[contains(text(), "Login Now")]')
    ))
    login_button.click()

    # 处理滑块验证（简化版，实际可能需要更复杂的处理）

    # ========== 3. 处理滑块验证 ==========



# ========== 尝试点击 Cookie 弹窗的 "Accept" 按钮 ==========
def close_cookie_popup():
    try:
        accept_button = driver.find_element(By.ID, "hs-eu-confirmation-button")
        if accept_button.is_displayed():
            accept_button.click()
            time.sleep(1)  # 等待页面重新布局
    except:
        pass  # 如果未找到或点击失败，忽略继续执行


# ========== 使用 requests 请求接口 ==========
def request_api_with_cookies():
    # 从 Selenium 获取 cookies
    cookies = driver.get_cookies()
    session_cookies = {cookie['name']: cookie['value'] for cookie in cookies}
    print(session_cookies)

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Referer": "https://www.gigab2b.com/",
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.9",
    }
    payload = {
        "page": 1,
        "limit": 100,
        "dimension_type": 1,
        "scene": 2,
        "sort": "",
        "order": "",
        "product_category_id": [10015]
    }

    url = "https://www.gigab2b.com/index.php?route=/product/list/search"

    response = requests.post(url, headers=headers, json=payload, cookies=session_cookies)

    print("状态码:", response.status_code)
    print("响应内容:", response.text[:500])  # 打印前500字符，防止过长

    if response.status_code == 200:
        try:
            result = response.json()
            product_list = result.get("data", {}).get("product_list", [])
            print("✅ 获取到的 product_list：")
            print(product_list)
        except Exception as e:
            print("❌ 解析返回 JSON 时出错：", e)
    else:
        print(f"❌ 请求失败，状态码：{response.status_code}")
        print(response.text)


# ========== 主入口 ==========
if __name__ == "__main__":
    login()
    time.sleep(3)
    close_cookie_popup()
    request_api_with_cookies()
    driver.quit()
