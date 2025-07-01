from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import time
import random

import urllib.parse
import pymysql  # 或使用 SQLAlchemy，

#
db = pymysql.connect(
    host="localhost",
    user="root",
    password="warehouse_nw",
    database="warehouse",
    charset="utf8mb4"
)
cursor = db.cursor()

# ========== 初始化 WebDriver ==========
options = Options()
options.add_argument('--start-maximized')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": "Object.defineProperty(navigator, 'webdriver', { get: () => undefined })"
})

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

    # 处理滑块验证（）

    # ========== 3. 处理滑块验证 ==========
    try:
        # 等待滑块验证元素加载
        time.sleep(2)  # 等待页面加载完成

        # 找到滑块容器和滑块元素
        slider_container = wait.until(EC.presence_of_element_located(
            (By.ID, "nc_1_n1t")
        ))

        slider = wait.until(EC.presence_of_element_located(
            (By.ID, "nc_1_n1z")
        ))

        # 获取滑块容器的位置和宽度
        container_location = slider_container.location
        container_x = container_location['x']
        container_width = slider_container.size['width']

        # 获取滑块的位置和宽度
        slider_location = slider.location
        slider_x = slider_location['x']
        slider_width = 20  # 假设滑块宽度为20px，可能需要根据实际情况调整

        # 计算需要滑动的距离（从滑块当前位置到容器右边界）
        current_slider_position = slider_x - container_x
        target_position = container_width - slider_width
        slide_distance = target_position - current_slider_position

        # 创建ActionChains对象
        actions = ActionChains(driver)

        # 点击并按住滑块
        actions.click_and_hold(slider).perform()

        #
        # 1. 开始时的随机停顿
        time.sleep(random.uniform(0.2, 0.5))

        # 2. 开始滑动，但加入不规则的停顿和抖动
        remaining_distance = slide_distance
        steps = random.randint(10, 20)  # 随机步数

        # 初始移动速度较快
        initial_fast_steps = random.randint(3, 5)
        fast_step_distance = remaining_distance * 0.6 / initial_fast_steps

        for i in range(initial_fast_steps):
            # 水平移动
            jitter_x = random.uniform(-1, 1)
            # 垂直移动 (非常微小的随机移动)
            jitter_y = random.uniform(-0.5, 0.5)

            actions.move_by_offset(jitter_x, jitter_y).perform()
            time.sleep(random.uniform(0.05, 0.15))

            # 移动主要方向
            actions.move_by_offset(fast_step_distance, 0).perform()
            time.sleep(random.uniform(0.1, 0.3))

            remaining_distance -= fast_step_distance

        # 3. 中间部分减速并加入更多抖动
        medium_steps = random.randint(3, 7)
        medium_step_distance = remaining_distance * 0.3 / medium_steps

        for i in range(medium_steps):
            # 更大的随机抖动
            jitter_x = random.uniform(-2, 2)
            jitter_y = random.uniform(-1, 1)

            actions.move_by_offset(jitter_x, jitter_y).perform()
            time.sleep(random.uniform(0.1, 0.2))

            # 移动主要方向
            actions.move_by_offset(medium_step_distance, 0).perform()
            time.sleep(random.uniform(0.15, 0.3))

            remaining_distance -= medium_step_distance

        # 4. 最后部分非常缓慢并加入回拉动作
        final_steps = random.randint(2, 4)
        final_step_distance = remaining_distance / final_steps

        for i in range(final_steps):
            #
            jitter_x = random.uniform(-3, 3)
            jitter_y = random.uniform(-1.5, 1.5)

            actions.move_by_offset(jitter_x, jitter_y).perform()
            time.sleep(random.uniform(0.15, 0.3))

            # 移动主要方向
            actions.move_by_offset(final_step_distance, 0).perform()
            time.sleep(random.uniform(0.2, 0.4))

            remaining_distance -= final_step_distance

        # 5. 额外的微小移动确保滑块到达最右端
        actions.move_by_offset(2, 0).perform()
        time.sleep(random.uniform(0.1, 0.2))

        # 6.
        backtrack_distance = random.uniform(2, 5)
        actions.move_by_offset(-backtrack_distance, 0).perform()
        time.sleep(random.uniform(0.1, 0.2))

        # 7. 再次向前滑动，完成验证
        actions.move_by_offset(backtrack_distance + 1, 0).perform()
        time.sleep(random.uniform(0.1, 0.2))

        # 释放滑块
        actions.release().perform()

        # 等待验证完成
        time.sleep(random.uniform(3, 5))  # 随机等待时间

        # 可以添加检查验证是否成功的逻辑
        # 例如检查某个元素是否出现或消失
    except TimeoutException:
        print("没有检测到滑块，继续执行")

    except Exception as e:
        print(f"滑块验证处理时出错: {str(e)}")
        # 即使验证失败，也继续执行后续代码
        # 实际应用中可能需要更复杂的错误处理





# ========== 主入口 ==========
if __name__ == "__main__":
    login()
    time.sleep(3)
    driver.quit()
