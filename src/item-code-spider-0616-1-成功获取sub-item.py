from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import time
import random

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


# ========== 爬取商品 ==========
def crawl_products():
    first_menus = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//span[@class="category-name text-word"]')))
    for first_item in first_menus:
        first_text = first_item.text.strip()
        print("\n一级菜单：", first_text)
        actions.move_to_element(first_item).perform()
        time.sleep(3)

        try:
            second_menus = driver.find_elements(By.XPATH, '//div[contains(@class,"second-level-category")]//div[@data-gmd-attr-search_keyword]')
            for second_item in second_menus:
                second_text = second_item.get_attribute('data-gmd-attr-search_keyword')
                print("  二级菜单：", second_text)
                actions.move_to_element(second_item).perform()
                time.sleep(2)

                third_menus = driver.find_elements(By.XPATH, '//div[contains(@class,"third-level-category")]//div[@data-gmd-attr-search_keyword]')
                for third_item in third_menus:
                    third_text = third_item.get_attribute('data-gmd-attr-search_keyword')
                    print("    三级菜单：", third_text)

                    third_item.click()
                    time.sleep(3)
                    crawl_product_list()
                    driver.back()
                    time.sleep(2)

        except Exception as e:
            print(f"处理 {first_text} 时出错: {str(e)}")

# ========== 商品列表页 ==========
def crawl_product_list():
    wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-v-40a32fa8 and contains(@class,"product-list")]')))
    product_items = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@data-v-3f3fee58 and contains(@class,"product-list-item")]')))

    for product_item in product_items:
        try:
            link = product_item.find_element(By.XPATH, './/a[@data-gmd-ck="item_click"]')
            link.send_keys(Keys.CONTROL + Keys.ENTER)
            time.sleep(1)
            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(2)
            crawl_product_detail()
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        except Exception as e:
            print(f"处理商品时出错: {str(e)}")

    handle_pagination()

# ========== 商品详情页 ==========
def crawl_product_detail():
    try:
        try:
            item_code_container = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[@class="items"]//span[contains(text(),"Item Code:")]/..'))
            )
            # 再定位 title 元素
            item_code_span = item_code_container.find_element(By.XPATH, './span[@title]')
            item_code = item_code_span.get_attribute('title')
            print(f"      Item Code: {item_code}")
        except:
            print("      Item Code: 未找到")
            with open("debug_detail.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            driver.save_screenshot("debug_detail.png")

        try:
            # 等待包含 Sub-item 的特征 div 出现
            container = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[contains(@class,'mt-12px') and div[contains(@class,'color-#333333')]]")
                )
            )
            sub_item_blocks = container.find_elements(By.XPATH,
                                                      './/div[contains(@class,"color-#333333") and contains(@class,"mb-16px")]')

            if not sub_item_blocks:
                print("页面无 Sub-item 信息，跳过")
            else:
                for block in sub_item_blocks:
                    spans = block.find_elements(By.TAG_NAME, 'span')
                    if len(spans) >= 3:
                        sub_item_raw = spans[0].text.strip()
                        sub_item = sub_item_raw.split(":", 1)[1].strip() if ":" in sub_item_raw else sub_item_raw
                        package_qty_raw = spans[1].text.strip()
                        package_qty = package_qty_raw.split(":", 1)[
                            1].strip() if ":" in package_qty_raw else package_qty_raw
                        size_weight = spans[2].text.strip()
                        print(f"Sub-item: {sub_item}")
                        print(f"Package Quantity: {package_qty}")


        except TimeoutException as e:
            pass
        except Exception as e:
            import traceback
            print("获取 Sub-item 信息失败:", traceback.format_exc())


    except Exception:
        print("      商品详情加载失败")

# ========== 分页处理 ==========
def handle_pagination():
    try:
        pagination = wait.until(EC.presence_of_element_located((By.XPATH, '//ul[@class="el-pager"]')))
        page_items = pagination.find_elements(By.XPATH, './/li[@class="number"]')
        max_page = int(page_items[-2].text)
        print(f"      总页数: {max_page}")

        for page in range(2, min(3, max_page) + 1):
            try:
                page_item = driver.find_element(By.XPATH, f'//li[@class="number" and text()="{page}"]')
                page_item.click()
                time.sleep(3)
                crawl_product_list()
            except Exception as e:
                print(f"跳转第 {page} 页失败：{str(e)}")
    except Exception as e:
        print(f"分页处理失败：{str(e)}")

# ========== 程序入口 ==========
if __name__ == "__main__":
    login()
    time.sleep(3)
    crawl_products()
    driver.quit()
