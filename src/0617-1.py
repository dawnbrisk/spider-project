from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
import traceback
import gc
import psutil
import os

# ========== 初始化 WebDriver ==========
options = Options()

# ① Headless 模式（节省内存 + 隐藏界面）
options.add_argument('--headless=new')  # 推荐新 headless 模式（更稳定）
options.add_argument('--disable-gpu')   # Headless 时必须（Windows 特别需要）
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

        # 模拟更自然的人类滑动行为 - 更复杂的模式
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
            # 更大的随机抖动
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

        # 6. 可能会有轻微的回拉动作，模拟人类操作
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

# ========== 尝试点击 Cookie 弹窗的 "Accept" 按钮 ==========
def close_cookie_popup():
    try:
        accept_button = driver.find_element(By.ID, "hs-eu-confirmation-button")
        if accept_button.is_displayed():
            accept_button.click()
            time.sleep(1)  # 等待页面重新布局
    except:
        pass  # 如果未找到或点击失败，忽略继续执行

# ========== 抓取所有分类 ==========
def crawl_products():
    try:
        close_cookie_popup()
        # 【改动1】改为先定位所有一级菜单元素
        first_menus = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//span[@class="category-name text-word"]')))
        # 【改动2】用索引循环，避免直接遍历过时元素
        for i in range(len(first_menus)):
            # 【改动3】循环里每次重新定位一级菜单，保证元素是最新的
            first_menus = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//span[@class="category-name text-word"]')))
            first_item = first_menus[i]

            first_text = first_item.text.strip()
            print("\n一级菜单：", first_text)
            actions.move_to_element(first_item).perform()
            time.sleep(3)

            try:
                # 【改动4】重新定位二级菜单元素，避免使用过时元素
                second_menus = driver.find_elements(By.XPATH, '//div[contains(@class,"second-level-category")]//div[@data-gmd-attr-search_keyword]')
                # 【改动5】用索引循环二级菜单
                for j in range(len(second_menus)):
                    # 【改动6】每次循环重新定位二级菜单元素，保证最新
                    second_menus = driver.find_elements(By.XPATH, '//div[contains(@class,"second-level-category")]//div[@data-gmd-attr-search_keyword]')
                    second_item = second_menus[j]
                    second_text = second_item.get_attribute('data-gmd-attr-search_keyword')
                    print("  二级菜单：", second_text)
                    actions.move_to_element(second_item).perform()
                    time.sleep(2)

                    # 【改动7】同理重新定位三级菜单元素
                    third_menus = driver.find_elements(By.XPATH, '//div[contains(@class,"third-level-category")]//div[@data-gmd-attr-search_keyword]')
                    # 【改动8】用索引循环三级菜单
                    for k in range(len(third_menus)):
                        # 【改动9】循环中重新定位三级菜单，避免元素过时
                        third_menus = driver.find_elements(By.XPATH, '//div[contains(@class,"third-level-category")]//div[@data-gmd-attr-search_keyword]')
                        third_item = third_menus[k]
                        third_text = third_item.get_attribute('data-gmd-attr-search_keyword')
                        print("    三级菜单：", third_text)

                        third_item.click()
                        time.sleep(3)
                        handle_pagination()
                        driver.back()
                        time.sleep(2)
            except Exception as e:
                print(f"Processing {first_text} failed: {str(e)}")
    except Exception as e:
        print(f"Failed to crawl products: {str(e)}")


# ========== 分页处理（点击“下一页”按钮） ==========
def handle_pagination():
    page_count = 1  # 初始化页码计数器
    while True:
        try:



            wait.until(EC.presence_of_all_elements_located(
                (By.XPATH, '//div[@data-v-3f3fee58 and contains(@class,"product-list-item")]')
            ))

            product_items = driver.find_elements(By.XPATH, '//div[@data-v-3f3fee58 and contains(@class,"product-list-item")]')
            print(f"正在处理第 {page_count} 页，共 {len(product_items)} 个商品")

            # for product_item in product_items:
            #     try:
            #         link = product_item.find_element(By.XPATH, './/a[@data-gmd-ck="item_click"]')
            #         link.send_keys(Keys.CONTROL + Keys.ENTER)
            #         time.sleep(2)
            #         driver.switch_to.window(driver.window_handles[-1])
            #         #time.sleep(2)
            #         #crawl_product_detail()
            #         driver.close()
            #         driver.switch_to.window(driver.window_handles[0])
            #     except Exception as e:
            #         print(f"处理商品时出错: {str(e)}")

            # 下一页按钮
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//div[contains(@class,"cursor-pointer") and .//i[contains(@class,"el-icon-right")]]')
                )
            )
            driver.execute_script("arguments[0].scrollIntoView();", next_button)
            time.sleep(1)
            next_button.click()

            time.sleep(3)
            page_count += 1  # 页码加一
            # 每页处理完
            del next_button
            del product_items
            gc.collect()
            print_memory_usage()
        except TimeoutException:
            print("没有更多页了，分页结束")
            break
        except Exception as e:
            print(f"翻页失败: {str(e)}")
            break

# ========== 商品详情 ==========
def crawl_product_detail():
    try:
        # 是否有 Sub-item
        has_sub_item = False

        try:
            container = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[contains(@class,'mt-12px') and div[contains(@class,'color-#333333')]]")
                )
            )
            sub_item_blocks = container.find_elements(By.XPATH,'.//div[contains(@class,"color-#333333") and contains(@class,"mb-16px")]')

            if sub_item_blocks:
                has_sub_item = True
                for block in sub_item_blocks:
                    spans = block.find_elements(By.TAG_NAME, 'span')
                    if len(spans) >= 3:
                        sub_item_raw = spans[0].text.strip()
                        sub_item = sub_item_raw.split(":", 1)[1].strip() if ":" in sub_item_raw else sub_item_raw
                        package_qty_raw = spans[1].text.strip()
                        package_qty = package_qty_raw.split(":", 1)[1].strip() if ":" in package_qty_raw else package_qty_raw

                        print(f"      Sub-item: {sub_item}  package Quantity: {package_qty}")

            else:
                print("      页面无 Sub-item，跳过 Item Code")

        except:
            print("      无 Sub-item 信息")

        if has_sub_item:
            try:
                item_code_container = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//div[@class="items"]//span[contains(text(),"Item Code:")]/..'))
                )
                item_code_span = item_code_container.find_element(By.XPATH, './span[@title]')
                item_code = item_code_span.get_attribute('title')
                print(f"      Item Code: {item_code}")
            except:
                print("      Item Code 未找到")

    except Exception as e:
        print("商品详情解析失败：", traceback.format_exc())


# 获取内存使用情况
def print_memory_usage():
    try:
        children = chrome_driver_process.children(recursive=True)
        total_memory = chrome_driver_process.memory_info().rss
        for child in children:
            total_memory += child.memory_info().rss
        print(f"当前 WebDriver 及其子进程使用内存: {total_memory / 1024 / 1024:.2f} MB")
    except psutil.NoSuchProcess:
        print("进程已不存在")

# ========== 主入口 ==========
if __name__ == "__main__":
    login()
    time.sleep(3)
    crawl_products()
    driver.quit()
