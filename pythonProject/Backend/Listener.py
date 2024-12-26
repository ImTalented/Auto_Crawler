from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from seleniumwire import webdriver  # 导入 selenium-wire
import time
import json



# 配置 Selenium 和 Chrome Driver
def setup_browser(vis):
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--start-maximized")
    if vis == False:
        chrome_options.add_argument("--headless")  # 可选，是否隐藏浏览器
    chrome_options.add_experimental_option("detach", True)  # 调试模式

    # 使用 WebDriver Manager 自动配置 ChromeDriver
    service = Service(ChromeDriverManager(url="http://npm.taobao.org/mirrors/chromedriver").install())
    browser = webdriver.Chrome(service=service, options=chrome_options)
    return browser

def login(browser):
    login_url = "https://waimaie.meituan.com/new_fe/login_gw#/login"  # 替换为实际登录 URL
    browser.get(login_url)

    # 等待页面加载完成（根据实际页面的 DOM 元素替换）
    time.sleep(2)

    # 提示用户手动登录
    print("请手动完成登录，并在完成后关闭浏览器。")

    #改用，url是否发生变化来判断，用户是否登录成功
    initial_url = browser.current_url

    while True:
        try:
            # 获取当前页面 URL
            current_url = browser.current_url
            # 如果页面 URL 发生了变化，说明页面已经跳转
            if current_url != initial_url:
                print("页面 URL 已变化，登录完成或页面跳转。")
                break
        except Exception as e:
            print(f"检查页面 URL 时出现错误: {e}")
            break
        time.sleep(1)

    print("登录完成，脚本将继续执行。")
    return 0





# 登录目标网站
def first_login(browser):
    login_url = "https://waimaie.meituan.com/new_fe/login_gw#/login"  # 替换为实际登录 URL
    browser.get(login_url)

    # 等待页面加载完成（根据实际页面的 DOM 元素替换）
    time.sleep(2)

    # 提示用户手动登录
    print("请手动完成登录，并在完成后关闭浏览器。")

    # 等待直到你手动登录并关闭浏览器，注意，这种方法可能导致获取的cookie不完全，因为关窗口关太快了
    # while True:
    #     try:
    #         cookies = browser.get_cookies()
    #         # 检测浏览器窗口是否关闭
    #         browser.title  # 如果窗口关闭，将引发异常
    #     except:
    #         print("浏览器已关闭，登录完成。")
    #         break
    #     time.sleep(1)

    #改用，url是否发生变化来判断，用户是否登录成功
    initial_url = browser.current_url

    while True:
        try:
            # 获取当前页面 URL
            current_url = browser.current_url

            # 如果页面 URL 发生了变化，说明页面已经跳转
            if current_url != initial_url:
                print("页面 URL 已变化，登录完成或页面跳转。")
                time.sleep(6)
                cookies = browser.get_cookies()
                break
        except Exception as e:
            print(f"检查页面 URL 时出现错误: {e}")
            cookies = browser.get_cookies()
            break
        time.sleep(1)

    browser.quit()
    print("登录完成，脚本将继续执行。")
    return cookies

def second_login(cookies):
    # 登陆成功，现在隐藏浏览器
    browser = setup_browser(True)

    login_url = "https://waimaie.meituan.com/new_fe/login_gw#/login"  # 替换为实际登录 URL
    #先get浏览器，再导入cookie，不然会报错
    browser.get(login_url)

    # 加入之前的cookie
    # for cookie in cookies:
    #     print(cookie)
    #     #清除掉非".meituan.com"的cookie，因为url发生跳转，一些新的cookie也被意外捕获了，这部分不需要
    #     if cookie['domain'] == '.meituan.com':
    #         browser.add_cookie(cookie)

    # 调试，手动输入对应cookie ,下列从request获取的cookie无法通过登录验证，已经尝试过了
    # cookies = {
    #     'device_uuid': '!f4fbfac8-7bc4-41b3-92c5-e337569044af',
    #     'uuid_update': 'true',
    #     'wpush_server_url': 'wss://wpush.meituan.com',
    #     'shopCategory': 'food',
    #     'JSESSIONID': 'h8zpw161cjo62vck3znc1zw6'
    # }
    #
    # for name, value in cookies.items():
    #     cookie = {
    #         'name': name,
    #         'value': value,
    #         'domain': '.meituan.com',  # 根据网站的域名调整
    #         'path': '/',  # 默认路径
    #     }
    #     browser.add_cookie(cookie)

    return browser

def sep_login(browser):
    # 第一次登录网站
    cookies = first_login(browser)
    if not cookies:
        print("登录失败，请重新登录")
        return 0

    # 隐藏浏览器登陆，开始后台自动化操作
    browser = second_login(cookies)
    return browser




# 监听网络请求（CDP）
def intercept_requests(driver, target_url):
    # 开启 CDP 会话
    cdp = driver.execute_cdp_cmd
    cdp("Network.enable", {})

    print(f"正在监听 {target_url} 的请求...")

    # 定义回调函数，拦截请求
    def handle_request(event):
        request = event.get("params", {}).get("request", {})
        url = request.get("url", "")
        if target_url in url:
            print(f"捕获目标请求: {url}")
            print("Headers:", json.dumps(request.get("headers"), indent=4))
            print("Payload:", request.get("postData", "无 POST 数据"))
            print("-" * 50)

    # 注册事件监听
    driver.execute_cdp_cmd("Network.requestWillBeSent", {"listener": handle_request})

    # 持续监听一段时间
    time.sleep(10)

# 主函数
def main():
    #先可见浏览器，登陆完后再隐藏
    browser = setup_browser(True)

    try:
        #一体式登录
        login(browser)
        #分离式登录
        # browser = sep_login(browser)

        # 监听网络请求，指定目标 URL
        target_url = "https://waimaieapp.meituan.com/gw/bizdata/flow/single/origin/v2"  # 替换为你的目标 URL
        intercept_requests(browser, target_url)
    finally:
        browser.quit()

if __name__ == "__main__":
    main()



#店铺调试用cookies
    #  cookies = {
    #         'device_uuid': '!f4fbfac8-7bc4-41b3-92c5-e337569044af',
    #         'uuid_update': 'true',
    #         'wpush_server_url': 'wss://wpush.meituan.com',
    #         'shopCategory': 'food',
    #         'JSESSIONID': 'h8zpw161cjo62vck3znc1zw6'
    #     }