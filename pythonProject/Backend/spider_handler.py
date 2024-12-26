import requests
from bs4 import BeautifulSoup
import browser_cookie3

class AutoCookieWebScraper:
    """
    支持自动获取浏览器 Cookie 的爬虫
    """

    def __init__(self, base_url: str, headers: dict = None):
        """
        初始化爬虫类
        :param base_url: 基础 URL
        :param headers: HTTP 请求头，默认为常见的 User-Agent
        """
        self.base_url = base_url
        self.headers = headers if headers else {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }


    def parse_html(self, html: str, parser: str = "html.parser") -> BeautifulSoup:
        """
        解析 HTML 内容为 BeautifulSoup 对象
        """
        return BeautifulSoup(html, parser)

    def scrape(self, path: str, cookie: str = None) -> None:
        """
        主爬取方法
        :param path: 请求的 URL 路径
        :param params: 请求的 URL 参数（可选）
        """
        url = f"{self.base_url}{path}"

        # 使用 requests.Session() 来保持会话
        session = requests.Session()

        # 将登录cookie添加到会话中
        for cookie_name, cookie_value in cookie.items():
            session.cookies.set(cookie_name, cookie_value)

        # 发送请求到目标URL（例如，获取新cookie的页面）
        response = requests.get(url, headers=self.headers)

        # 获取新cookie
        new_cookies = session.cookies.get_dict()

        # 模拟发起请求，获取用户信息或其他所需的参数,不需要params，因为有cookie
        response = requests.get(url, headers=self.headers,cookies=new_cookies)

        if response.status_code == 200:
            print("请求成功")
            soup = self.parse_html(response.text)
            print("网页内容:", soup.prettify()[:500])  # 打印部分内容（可修改为你的逻辑）
            return soup
        else:
            print(f"请求失败，状态码: {response.status_code}")
            return 0

def start_crawler(cookie):
    # 各项参数如何填
    base_url = "https://waimaieapp.meituan.com"  # 设置为主机名部分，即主站的网址
    scraper = AutoCookieWebScraper(base_url)    #类初始化，即生成对象scraper

    # 设置请求路径和查询参数
    path = "/gw/bizdata/flow/single/origin/v2" # 用检索工具，抄录对应接口
    # 检索工具中的Payload，但是得手动改成字典序，可以叫gpt帮忙完成

    # 爬取需要登录的页面
    return scraper.scrape(path, cookie=cookie)



# #获取前端返回的登陆数据后，后端python实行模拟登陆，登陆成功后   （只能获取当前网页）
# def get_meituan_cookie(username):
#     """
#     模拟爬取目标网站并获取登录后的 Cookie
#     """
#     login_url = "https://waimaie.meituan.com/"
#     session = requests.Session()
#
#     # 示例：模拟登录的逻辑，这里需要具体分析目标网站登录请求
#     # 如果登录后会重定向，可以抓包确认请求逻辑
#     headers = {
#         "User-Agent": "Mozilla/5.0",
#         "Content-Type": "application/json",
#     }
#
#     # 这里可以根据实际情况向服务器发送一个有效请求
#     # 例如填充必要的用户名和 session 等参数
#     try:
#         response = session.get(login_url, headers=headers)
#         if response.status_code == 200:
#             cookie_dict = session.cookies.get_dict()
#             print("获取的 Cookie：", cookie_dict)
#             return cookie_dict
#         else:
#             return None
#     except Exception as e:
#         print(f"获取 Cookie 失败: {e}")
#         return None
#
