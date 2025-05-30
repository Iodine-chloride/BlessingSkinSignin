from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 配置 Chrome 浏览器选项
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')  # 无头模式
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.binary_location = "/usr/bin/chromium-browser"  # 指定 Chromium 路径

# 设置 ChromeDriver 服务
service = Service("/usr/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=chrome_options)

# 打开目标网页
driver.get('')  #输入目标皮肤站URL

# 登录操作
try:
    # 等待页面加载，等待邮箱输入框出现
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Email or player name']")))  # 等待邮箱输入框
    print("邮箱输入框已加载")

    # 填写登录信息
    email_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Email or player name']")
    password_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Password']")

    email_input.send_keys("")  # 输入用户名
    password_input.send_keys("")  # 输入密码

    print("输入了用户名和密码")

    # 提交登录表单
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    login_button.click()

    print("提交了登录表单")

    # 增加等待时间，确保页面完全加载
    time.sleep(5)

    # 再次检查页面是否发生变化，确认登录成功
    page_source = driver.page_source
    if "Login" not in page_source:  # 确认是否存在“登录”字样，如果页面已更新则说明登录成功
        print("登录成功！")
    else:
        print("登录失败，页面源代码：")
        print(page_source)
        
    # 登录成功后，执行签到操作
    try:
        # 等待签到按钮可点击
        sign_in_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button.btn.bg-gradient-primary.pl-4.pr-4"))
        )

        # 打印按钮的状态信息
        button_disabled = sign_in_button.get_attribute('disabled')
        button_text = sign_in_button.text
        print(f"按钮文本: {button_text}, 禁用状态: {button_disabled}")

        # 检查按钮是否禁用
        if button_disabled:
            print("按钮不可点击，等待一段时间...")
            time.sleep(3600)  # 等待1小时
        else:
            # 检查按钮的文本是否包含 "x 小时 后可签到"
            if "Available after" in button_text:
                print("按钮处于禁用状态，等待可点击。")
                time.sleep(3600)  # 等待1小时，可设置青龙最大执行时长直接终止任务
            else:
                sign_in_button.click()
                print("签到成功！")
    except Exception as e:
        print(f"签到操作发生错误: {e}")

except Exception as e:
    print(f"登录操作发生错误: {e}")
    # 输出详细的错误信息，帮助诊断
    print("发生错误时的页面源代码:")
    print(driver.page_source)

# 完成操作后退出浏览器
driver.quit()
