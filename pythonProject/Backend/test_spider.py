import time
import json
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.parse

class MeituanSpider:
    def __init__(self):
        self.login_url = 'https://waimaie.meituan.com/new_fe/login_gw#/login'
        self.login_url_2 = 'https://waimaie.meituan.com/logon'
        self.data_url = 'https://waimaie.meituan.com/?time=1735120753094&ignoreSetRouterProxy=true#https://waimaieapp.meituan.com/igate/bizdata/flowrate'  # 目标数据页面
        self.username = "dbj2025"  # 不预设用户名
        self.password = "dbj1234" # 不预设密码

        # 配置Selenium的Chrome浏览器选项（显示界面）
        self.options = Options()
        # self.options.add_argument('--no-sandbox')
        # self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36")

        # 配置DevTools协议，捕获HTTP请求日志
        self.options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

        # 启动浏览器并访问目标页面
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)
        self.driver.get(self.login_url)
    def login_and_capture_data(self):
        """
        登录并捕获目标页面请求的 Headers 和 Payload。
        登录完成后直接跳转到目标页面并捕获网络请求日志。
        """
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@id="login"]'))
        )

        # elements = self.driver.find_elements(By.TAG_NAME, 'button')
        # print(f"找到 {len(elements)} 个按钮")
        # for el in elements:
        #     print(el.get_attribute('outerHTML'))

        #自动化操作
        input_field = self.driver.find_element(By.ID, "login")
        input_field.send_keys("dbj2025")
        password_field = self.driver.find_element(By.ID, "password")
        password_field.send_keys("dbj1234")
        checkbox = self.driver.find_element(By.CLASS_NAME, "ep-checkbox-container")
        checkbox.click()
        button = self.driver.find_element(By.CLASS_NAME, "ep-login_btn")
        button.click()

        while True:
            time.sleep(3)
            current_url = self.driver.current_url
            if current_url != self.login_url and current_url != self.login_url_2:  # 判断URL是否变化
                print("登录成功，跳转到商户页面！")
                break

        # 登录成功后，获取 cookies
        cookies = self.driver.get_cookies()
        print("cookies",cookies)

        self.driver.get(self.data_url)
        time.sleep(10)
        self.driver.get("https://waimaieapp.meituan.com/igate/bizdata/flowrate")
        time.sleep(2)
        # time.sleep(3)
        # txt_element = self.driver.find_element(By.CLASS_NAME, 'txt_1wSopn')
        # txt_element.click()
        # time.sleep(6)
        #
        # time.sleep(1)
        # txt_element2 = self.driver.find_element(By.ID, '经营数据')
        # txt_element2.click()

        #展开表格
        # time.sleep(3)
        # elements = self.driver.find_elements(By.TAG_NAME, 'button')
        # print(f"找到 {len(elements)} 个按钮")
        # for el in elements:
        #     print(el.get_attribute('outerHTML'))

        # html = self.driver.execute_script("return document.documentElement.outerHTML;")
        # print(html)
        # with open("D:/Python_Auto_Tool/Auto_Crawler/page_source.html", "w", encoding="utf-8") as file:
        #     file.write(html)

        # print(self.driver.page_source)    //div[@class="customRoo-btn-group customRoo-btn-ltr customRoo-btn-radio-group" and @value="bubble"]


        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH,'//button[@title="表格"]'))
        )

        # 定位 value="table" 的元素
        table_option = self.driver.find_element(By.XPATH,'//button[@title="表格"]')

        # 点击切换到 table
        table_option.click()


        #实际上，只要获取第一页的payload，就能顺带把其他页数据也获取了
        # # 显式等待分页容器加载完成
        # WebDriverWait(self.driver, 10).until(
        #     EC.presence_of_element_located((By.CLASS_NAME, "roo-pagination"))
        # )
        #
        # # 定位分页容器
        # pagination = self.driver.find_element(By.CLASS_NAME, "roo-pagination")
        #
        # # 获取分页容器内的所有 <li> 元素
        # # 获取初始分页按钮数量
        # pagination_buttons = pagination.find_elements(By.TAG_NAME, "li")
        # total_pages = len(pagination_buttons)
        #
        # # 遍历所有分页按钮
        # for i in range(len(pagination_buttons)):
        #         # 重新获取分页按钮（防止 DOM 更新后失效）
        #         pagination_buttons = pagination.find_elements(By.TAG_NAME, "li")
        #
        #         # 获取按钮的 aria-label 属性
        #         pagination_buttons = pagination.find_elements(By.TAG_NAME, "li")
        #         aria_label = pagination_buttons[i].find_element(By.TAG_NAME, "a").get_attribute("aria-label")
        #         print("i和aria_label", i, aria_label)
        #
        #         # 如果是"上一页"或"下一页"按钮，则跳过
        #         if aria_label in ["Previous", "Next"]:
        #             print(f"跳过了前后翻页按钮：{aria_label}")
        #             continue
        #
        #         # 跳过当前激活的按钮（即已是当前页）
        #         if "active" in pagination_buttons[i].get_attribute("class"):
        #             print(f"跳过了当前激活的按钮：{aria_label}")
        #             continue
        #
        #         # 获取 <a> 标签
        #         a_tag = pagination_buttons[i].find_element(By.TAG_NAME, "a")
        #
        #         # 确保元素可点击
        #         WebDriverWait(self.driver, 10).until(
        #             EC.element_to_be_clickable(a_tag)
        #         )
        #
        #         # 将元素滚动到视窗中（如果它不在视窗内）
        #         self.driver.execute_script("arguments[0].scrollIntoView();", a_tag)
        #
        #         # 点击当前按钮
        #         # pagination_buttons = pagination.find_elements(By.TAG_NAME, "li")
        #         # a_tag = pagination_buttons[i].find_element(By.TAG_NAME, "a")
        #         # a_tag.click()
        #         time.sleep(6)
        #         self.driver.execute_script("arguments[0].click();", a_tag)
        #         print(f"点击了第 {i + 1} 页按钮")
        #
        #         # 等待页面加载完成（根据表格内容的更新判断）
        #         WebDriverWait(self.driver, 10).until(
        #             EC.presence_of_element_located((By.CSS_SELECTOR, "table"))  # 替换为表格的选择器
        #         )
        #
        #         # 可选：模拟等待（让页面有充分时间加载）
        #         time.sleep(2)


        # 获取性能日志
        logs = self.driver.get_log('performance')
        with open("D:/Python_Auto_Tool/Auto_Crawler/performance_logs.json", "w", encoding="utf-8") as file:
            json.dump(logs, file, ensure_ascii=False, indent=4)

        print("日志已成功保存到 performance_logs.json")

        # 2. 用来保存筛选结果的列表
        filtered_urls = []

        # 3. 遍历日志
        for entry in logs:
            try:
                # 3.1 将 entry['message'] 转换为字典
                message_json = json.loads(entry['message'])

                # 3.2 取到 message
                message = message_json.get('message', {})

                # 3.3 判断是否是网络请求事件（Network.requestWillBeSent 或 Network.responseReceived）
                method = message.get('method', '')
                if method == 'Network.requestWillBeSent':
                    # 3.4 获取请求的详细参数
                    params = message.get('params', {})
                    request = params.get('request', {})
                    url = request.get('url', '')

                    # 3.5 判断 url 中是否包含目标字符串
                    if "https://waimaieapp.meituan.com/gw/bizdata/flow/compass/rank?token=" in url:
                        filtered_urls.append(url)
            except Exception as e:
                # 发生异常时可以选择打印或直接忽略
                # print(f"Log parse error: {e}")
                pass
        print(filtered_urls)

        return cookies

    def send_request(self, cookies):
        """
        使用 Requests 库模拟后续请求，发送 Headers 和 Payload。
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Cookie': '; '.join([f"{cookie['name']}={cookie['value']}" for cookie in cookies]),
        }

        # 发送 POST 请求（模拟业务请求）
        payload = {
            'param1': 'value1',
            'param2': 'value2',
        }

        # 发送请求并获取页面内容
        response = requests.post(self.data_url, headers=headers, data=payload)
        return response

    def parse_data(self, response):
        """
        解析 HTML 内容并提取需要的数据。
        """
        soup = BeautifulSoup(response.text, 'html.parser')

        # 根据实际页面结构提取需要的数据
        # 假设你要提取表格数据
        table = soup.find('table')
        rows = table.find_all('tr')
        for row in rows:
            columns = row.find_all('td')
            data = {
                'name': columns[0].text.strip(),
                'price': columns[1].text.strip(),
            }
            print(data)  # 或者保存到文件/数据库

    def run(self):
        """
        执行爬虫任务：登录、捕获请求日志、发送请求、解析数据。
        """
        # 登录并捕获数据
        cookies = self.login_and_capture_data()

        # 使用cookies发送请求
        response = self.send_request(cookies)

        # # 解析返回的页面数据
        # self.parse_data(response)

        # 关闭浏览器
        self.driver.quit()

# 执行爬虫任务
if __name__ == '__main__':
    spider = MeituanSpider()
    spider.run()
