from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
import mysql.connector
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
# ========== 1. 启动 WebDriver ==========


options = Options()
options.add_argument('--start-maximized')

# 正确方式：用 Service 包装 ChromeDriverManager
service = Service(ChromeDriverManager().install())

driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 15)

# ========== 2. 登录 ==========
# 打开登录页面
driver.get("https://www.gigab2b.com/index.php?route=account/login")

# 填写邮箱
email_input = wait.until(EC.visibility_of_element_located(
    (By.XPATH, '//input[@placeholder="Email"]')
))
email_input.send_keys("demo@buyer.com")

# 填写密码
password_input = wait.until(EC.visibility_of_element_located(
    (By.XPATH, '//input[@placeholder="Password"]')
))
password_input.send_keys("!u67q12dM")

# 点击“Login Now”按钮
login_button = wait.until(EC.element_to_be_clickable(
    (By.XPATH, '//button[contains(text(), "Login Now")]')
))
login_button.click()
# ========== 3. 等待登录成功 ==========
actions = ActionChains(driver)

# 获取所有一级菜单
first_level_items = wait.until(EC.presence_of_all_elements_located(
    (By.XPATH, '//span[@class="category-name text-word"]')
))

for first_item in first_level_items:
    first_text = first_item.text.strip()
    print("一级菜单：", first_text)

    # 悬浮一级菜单
    actions.move_to_element(first_item).perform()
    time.sleep(1)

    try:
        # 获取所有二级菜单（已展开）
        second_level_items = wait.until(EC.presence_of_all_elements_located((
            By.XPATH,
            '//div[contains(@class,"second-level-category")]//div[contains(@class,"category-name")]'
        )))

        for second_item in second_level_items:
            second_text = second_item.text.strip()
            print("  二级菜单：", second_text)

            actions.move_to_element(second_item).perform()
            time.sleep(1)

            # 获取三级菜单，类似思路
            third_level_items = driver.find_elements(By.XPATH,
                                                     '//div[contains(@class,"third-level-category")]//div[contains(@class,"category-name")]')
            for third_item in third_level_items:
                third_text = third_item.text.strip()
                print("    三级菜单：", third_text)
    except Exception as e:
        print(f"跳过 {first_text} → {e}")

# ========== 8. 关闭 ==========
driver.quit()
