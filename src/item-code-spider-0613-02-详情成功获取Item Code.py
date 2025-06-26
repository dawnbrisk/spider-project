from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import mysql.connector
import time
import random
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains

# ========== 1. 启动 WebDriver ==========
options = Options()
options.add_argument('--start-maximized')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
    Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
    })
    """
})

wait = WebDriverWait(driver, 15)


# ========== 2. 登录 ==========
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


# ========== 3. 爬取商品数据 ==========
def crawl_products():
    # 获取所有一级菜单
    first_level_items = wait.until(EC.presence_of_all_elements_located(
        (By.XPATH, '//span[@class="category-name text-word"]')
    ))

    for first_item in first_level_items:
        first_text = first_item.text.strip()
        print("\n一级菜单：", first_text)

        # 悬浮一级菜单
        actions = ActionChains(driver)
        actions.move_to_element(first_item).perform()
        time.sleep(4)

        try:
            # 获取二级菜单
            second_level_items = driver.find_elements(By.XPATH,
                                                      '//div[contains(@class,"second-level-category")]//div[contains(@class,"customer-scrollbar")]//div[@data-gmd-attr-search_keyword]'
                                                      )

            for second_item in second_level_items:
                second_text = second_item.get_attribute('data-gmd-attr-search_keyword')
                print("  二级菜单：", second_text)

                # 悬浮二级菜单以展开三级菜单
                actions.move_to_element(second_item).perform()
                time.sleep(3)

                # 获取三级菜单
                third_level_items = driver.find_elements(By.XPATH,
                                                         '//div[contains(@class,"third-level-category")]//div[contains(@class,"third-level-box")]//div[@data-gmd-attr-search_keyword]'
                                                         )

                for third_item in third_level_items:
                    third_text = third_item.get_attribute('data-gmd-attr-search_keyword')
                    print("    三级菜单：", third_text)

                    # 点击三级菜单进入商品列表页
                    third_item.click()
                    time.sleep(3)

                    # 爬取商品列表
                    crawl_product_list()

                    # 返回上级页面
                    driver.back()
                    time.sleep(2)

        except Exception as e:
            print(f"处理 {first_text} 时出错: {str(e)}")


# ========== 4. 爬取商品列表页 ==========
def crawl_product_list():
    # 等待商品列表加载
    product_list = wait.until(EC.presence_of_element_located(
        (By.XPATH, '//div[@data-v-40a32fa8 and contains(@class,"product-list")]')
    ))

    # 获取当前页商品
    product_items = wait.until(EC.presence_of_all_elements_located(
        (By.XPATH, '//div[@data-v-3f3fee58 and contains(@class,"product-list-item")]')
    ))

    for product_item in product_items:
        try:
            # 点击商品图片在新标签页打开
            product_link = product_item.find_element(By.XPATH, './/a[@data-gmd-ck="item_click"]')
            product_link.send_keys(Keys.CONTROL + Keys.ENTER)  # 在新标签页打开
            time.sleep(1)

            # 切换到新标签页
            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(2)

            # 爬取商品详情
            crawl_product_detail()

            # 关闭当前标签页，切换回主标签页
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(1)

        except Exception as e:
            print(f"处理商品时出错: {str(e)}")
            continue

    # 处理分页
    handle_pagination()


# ========== 5. 爬取商品详情页 ==========
def crawl_product_detail():
    print("      -----------------------------          ")

    try:
        # 等待商品详情加载
        wait.until(EC.presence_of_element_located(
            (By.XPATH, '//div[@data-v-e6a90129 and contains(@class,"text-20px text-bold")]')
        ))

        # 获取Item Code
        try:
            item_code_element = driver.find_element(By.XPATH,
                                                    '//span[@class="color-#666666 text-14px" and contains(text(),"Item Code:")]'
                                                    '/following-sibling::span[@class="color-#333333 text-14px ml-6px text-overflow"]'
                                                    )
            item_code = item_code_element.get_attribute('title')
            print(f"      Item Code: {item_code}")
        except:
            try:
                item_code_element = driver.find_element(By.XPATH,
                                                        '//div[@data-v-e6a90129 and contains(@class,"items")]'
                                                        '/span[@class="color-#666666 text-14px" and contains(text(),"Item Code:")]'
                                                        '/following-sibling::span[@class="color-#333333 text-14px m1-6px text-overflow"]'
                                                        )
                item_code = item_code_element.get_attribute('title')
                print(f"      Item Code: {item_code}")
            except:
                print("      Item Code: 未找到")

        # 获取Sub-item和Package Quantity
        try:
            explicit_wait  = WebDriverWait(driver, 10)
            sub_items_container = explicit_wait .until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(@class,"mt-12px")]'))
            )

            sub_item_blocks = sub_items_container.find_elements(By.XPATH,
                                                                './/div[contains(@class, "mb-16px")]')

            print(f"      找到 {len(sub_item_blocks)} 个子项")

            for block in sub_item_blocks:
                try:
                    spans = block.find_elements(By.TAG_NAME, 'span')
                    if len(spans) >= 3:
                        sub_item_text = spans[0].text
                        sub_item_value = sub_item_text.split(":", 1)[1].strip()

                        package_qty_text = spans[1].text
                        package_qty_value = package_qty_text.split(":", 1)[1].strip()

                        size_weight_text = spans[2].text.strip()

                        print(f"      Sub-item: {sub_item_value}")
                        print(f"      Package Quantity: {package_qty_value}")
                        print(f"      尺寸重量: {size_weight_text}")
                    else:
                        print(f"        未找到完整的 span 信息")
                except Exception as e:
                    print(f"        处理Sub-item单个子项时出错: {str(e)}")

        except Exception as e:
            print(f"      获取Sub-item子项信息时出错: {str(e)}")

    except:
        print(f"      获取商品详情时出错")  # ✅ 这个 now is correctly indented


# ========== 6. 处理分页 ==========
def handle_pagination():
    # 等待分页组件加载
    pagination = wait.until(EC.presence_of_element_located(
        (By.XPATH, '//ul[@class="el-pager"]')
    ))

    # 获取所有页码
    page_items = pagination.find_elements(By.XPATH, './/li[@class="number"]')
    max_page = int(page_items[-2].text)  # 倒数第二个是最大页码(因为最后一个可能是"50")
    print(f"      总页数: {max_page}")

    # 可以选择爬取所有页或指定页数
    for page in range(1, min(max_page, 3) + 1):  # 示例:只爬取前3页
        if page > 1:
            # 点击下一页或特定页码
            if page <= 6:  # 前6页有直接数字
                page_item = pagination.find_element(By.XPATH, f'.//li[@class="number" and text()="{page}"]')
            else:  # 第7页及以后需要点击"更多"按钮
                more_button = driver.find_element(By.XPATH, '//li[@class="el-icon more btn-quicknext el-icon-more"]')
                more_button.click()
                time.sleep(1)
                page_item = pagination.find_element(By.XPATH, f'.//li[@class="number" and text()="{page}"]')

            page_item.click()
            time.sleep(3)  # 等待页面加载

            # 重新爬取当前页商品(因为页面已刷新)
            crawl_product_list()


# ========== 7. 主程序 ==========
if __name__ == "__main__":
    from selenium.webdriver.common.keys import Keys

    login()
    time.sleep(3)
    crawl_products()
    driver.quit()