from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import MoveTargetOutOfBoundsException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

from PIL import Image
import io
import math
import os
import time

def smart_capture_element(driver, output_path='screenshot.png', css_selector="div.mes_text"):
    try:
        # # 配置 Edge 浏览器
        # options = Options()
        # # options.add_argument("--headless")
        # options.add_argument("--disable-gpu")
        # service = Service(r"E:\Code\msedgedriver.exe")
        # driver = webdriver.Edge(service=service, options=options)
        # driver.set_window_size(1920, 1000)
        # driver.get(url)
        # time.sleep(3)
        # element = driver.find_element(By.ID, "rightNavHolder")
        # ActionChains(driver).move_to_element(element).click().perform()
        # time.sleep(1)
        # elm2 =driver.find_element(By.ID,"CharID0")
        # ActionChains(driver).move_to_element(elm2).click().perform()
        
        # # 使用显式等待定位元素
        # time.sleep(5)
        wait = WebDriverWait(driver, 5)
        all_mes_text = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.mes.last_mes"))# By.CLASS_NAME, "element_class"
            # EC.presence_of_all_elements_located((By.CLASS_NAME, "mes_text"))
            )
        element = all_mes_text[-1]


        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth'});", element)
        # driver.execute_script("arguments[0].style.border='3px solid red';", element)  # 调试用红色边框

        # 动态获取元素尺寸
        element_height = driver.execute_script("return arguments[0].scrollHeight", element)
        viewport_height = driver.execute_script("return window.innerHeight")
        device_pixel_ratio = driver.execute_script("return window.devicePixelRatio")
        
        if element_height <= 0:
            raise ValueError("❌ 元素高度为0，请检查页面内容")

        # 智能截图决策
        if element_height <= viewport_height * 1.2:
            # 直接截图
            element.screenshot(output_path)
            print("🟢 使用直接截图方式")
        else:
            # 滚动截图
            element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.mes.last_mes'))
        )
        
            try:
                print("🟡 使用滚动截图方式")
                # 强制显示元素（应对隐藏情况）
                driver.execute_script("""
                    arguments[0].style.cssText = 
                        'display: block !important;' +
                        'visibility: visible !important;' +
                        'overflow: visible !important;';
                """, element)
                
                # 获取元素真实尺寸
                rect = driver.execute_script("""
                    const rect = arguments[0].getBoundingClientRect();
                    return {
                        width: Math.ceil(rect.width),
                        height: Math.ceil(rect.height),
                        top: rect.top,
                        left: rect.left
                    };
                """, element)
                
                print(f"元素尺寸: {rect['width']}x{rect['height']}px")

                # 调整窗口大小以完整包含元素
                driver.set_window_size(
                    1280,
                    7000
                )
                
                # 等待窗口调整完成
                time.sleep(1)
                
                # 方法1：直接使用元素截图（推荐）
                element.screenshot(output_path)
                
                # 方法2：备用方案（如果方法1失效）
                if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
                    full_screenshot = driver.get_screenshot_as_png()
                    with open(output_path, 'wb') as f:
                        f.write(full_screenshot)
                
                print(f"✅ 截图保存至: {os.path.abspath(output_path)}")
                driver.set_window_size(1920, 1000)
                return output_path

            except Exception as e:
                print(f"❌ 错误: {str(e)}")
                if driver:
                    driver.save_screenshot('error_screenshot.png')  # 保存错误状态截图
                raise
        print(f"✅ 截图保存至: {os.path.abspath(output_path)}")
        return output_path

    except Exception as e:
        print(f"❌ 错误: {str(e)}")
        if driver:
            driver.quit()
        raise