import requests
from bs4 import BeautifulSoup
import browser_cookie3
import pandas as pd
import os
from datetime import datetime, timedelta

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

    # def get_cookies(self):
    #     """
    #     从浏览器自动获取 Cookie
    #     """
    #     try:
    #         # ################ 记得把89780改了
    #         return browser_cookie3.chrome(cookie_file='C:\\Users\\89780\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Network\\Cookies', domain_name=self.base_url)
    #     except Exception as e:
    #         print(f"获取 Cookie 失败: {e}")
    #         return None

    # def fetch_page(self, url: str) -> str:
    #     """
    #     获取网页 HTML 内容
    #     """
    #     print("123412")
    #     cookies = self.get_cookies()
    #     if not cookies:
    #         print("无法获取 Cookie，无法访问网页")
    #         return ""
    #
    #     try:
    #         response = requests.get(url, headers=self.headers, cookies=cookies)
    #         response.raise_for_status()  # 检查请求是否成功
    #         return response.text
    #     except requests.RequestException as e:
    #         print(f"获取网页出错: {url}, 错误信息: {e}")
    #         return ""

    def parse_html(self, html: str, parser: str = "html.parser") -> BeautifulSoup:
        """
        解析 HTML 内容为 BeautifulSoup 对象
        """
        return BeautifulSoup(html, parser)


    def excel_out_1(self, positions_datas: dict = None):
        # 为每个位置生成一个单独的 Excel 文件
        output_directory = r'D:\Python_Auto_Tool\Auto_Crawler\positions_data_files\\'



        # 遍历 positions_data，生成 Excel 文件
        for position in positions_datas:
            data = []
            position_name = position['position']  # 获取位置名称
            position_data = position['data']  # 获取该位置的数据
            print("position_name",position_name)

            expose_count = position_data.get('exposeCnt', 0)
            visit_count = position_data.get('visitCnt', 0)
            click_rate = position_data.get('clickRate', 0)

            # 将数据添加到结果列表
            data.append({
                '曝光量': expose_count,
                '访问量': visit_count,
                '点击率': click_rate
            })



            current_date = datetime.now() - timedelta(days=1)
            date_str = current_date.strftime('%Y-%m-%d')  # 格式化为 'YYYY-MM-DD'

            # 将日期列添加到数据中
            for entry in data:
                entry['date'] = date_str  # 添加日期到每个数据点

            # 将数据转换为 DataFrame
            df = pd.DataFrame(data)

            # 设置日期为索引
            df.set_index('date', inplace=True)

            # 输出文件路径
            output_file = os.path.join(output_directory, f'{position_name}.xlsx')

            # 如果文件已存在，则追加数据
            if os.path.exists(output_file):
                with pd.ExcelWriter(output_file, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
                    df.to_excel(writer, sheet_name=position_name)
            else:
                # 如果文件不存在，创建新的 Excel 文件
                with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                    df.to_excel(writer, sheet_name=position_name)

            print(f"数据已保存到: {output_file}")

        print("所有数据已成功导出！")

    def excel_out_2(self, positions_data: dict = None):
        data = []

        # 遍历 positions_data，将数据转换为需要的格式
        for position in positions_data:
            position_name = position['position']  # 获取位置名称
            position_data = position['data']  # 获取位置对应的数据

            # 获取具体的数据
            expose_count = position_data.get('exposeCnt', 0)
            visit_count = position_data.get('visitCnt', 0)
            click_rate = position_data.get('clickRate', 0)

            # 将数据添加到结果列表
            data.append({
                '位置': position_name,
                '曝光量': expose_count,
                '访问量': visit_count,
                '点击率': click_rate
            })

        # 将数据转换为 DataFrame
        df = pd.DataFrame(data)

        # 导出到 Excel 文件
        output_file = r'D:\Python_Auto_Tool\Auto_Crawler\positions_data.xlsx'
        df.to_excel(output_file, index=False)

        print(f"数据已导出到 {output_file}")

    def scrape(self, path: str, params: dict = None) -> None:
        """
        主爬取方法
        :param path: 请求的 URL 路径
        :param params: 请求的 URL 参数（可选）
        """
        url = f"{self.base_url}{path}"
        if params:
            response = requests.get(url, headers=self.headers, params=params)
        else:
             response = requests.get(url, headers=self.headers)


        print(response.cookies,123)
        if response.status_code == 200:
            print("请求成功")
            soup = self.parse_html(response.text)
            print("网页内容:", soup.prettify()[:500])  # 打印部分内容（可修改为你的逻辑）
        else:
            print(f"请求失败，状态码: {response.status_code}")







if __name__ == "__main__":
    # 各项参数如何填
    base_url = "https://waimaieapp.meituan.com"  # 设置为主机名部分，即主站的网址
    scraper = AutoCookieWebScraper(base_url)    #类初始化，即生成对象scraper

    # 设置请求路径和查询参数
    path = "/gw/bizdata/flow/compass/rank" # 用检索工具，抄录对应接口
    # 检索工具中的Payload，但是得手动改成字典序，可以叫gpt帮忙完成
    params = {
        "token": "0OdhVz3ySGaI824b-RtbT8P2VnBdUdbjVifNN8uTejq0*",
        "wmPoiId": -1,
        "acctId": 217372828,
        "appType": 3,
        "orderBy": "EXP",
        "desc": True,
        "pageNum": 1,
        "pageSize": 20,
        "wmPoiIds": "",
        "durationType": 1,
        "bizLineType": 0,
        "dt": 20241225,
        "compareType": 0,
        "checkedAcctId": -999,
        "gray": True,
        "cityId": -999,
        "poiFlowType": 0,
        "match": {
            "path": "/igate/bizdata/flowrate",
            "url": "/igate/bizdata/flowrate",
            "isExact": True,
            "params": {}
        },
        "location": {
            "pathname": "/igate/bizdata/flowrate",
            "search": "",
            "hash": "",
            "key": "zm60sb"
        },
        "history": {
            "length": 5,
            "action": "PUSH",
            "location": {
                "pathname": "/igate/bizdata/flowrate",
                "search": "",
                "hash": "",
                "key": "zm60sb"
            }
        },
        "ignoreSetRouterProxy": True,
        "yodaReady": "h5",
        "csecplatform": 4,
        "csecversion": "2.4.0",
        "mtgsig": {
            "a1": "1.1",
            "a2": 1735203995323,
            "a3": "20y253ux9w20595317xzz60y33u0w6uw80603550w7197958wu6vzw08",
            "a5": "Cb9Gc6YvBIQVLleBdtoOgZ==",
            "a6": "hs1.4RhXRbf95/GVxNtwgxEz6dp08KCxtXZ7O/2yDB1/6vnkZSvwH+2srGDM20M3ERdvUuQOqRuknS6fRGG1Av4ChOQ==",
            "x0": 4,
            "d1": "07e01ae78bbde4c4df33993b8c5dfe61"
        }
    }


    # 爬取需要登录的页面
    scraper.scrape(path, params=params)




"""
信息汇总
Request URL:https://waimaieapp.meituan.com/gw/bizdata/flow/single/origin/v2?token=0htOuf1eAVTbQaMBK3QAX2GtljWt2JYI6sDdm24Cj-l0*&wmPoiId=20089767&acctId=179220072&appType=3&durationType=1&dt=&ignoreSetRouterProxy=true&yodaReady=h5&csecplatform=4&csecversion=2.4.0&mtgsig=%7B%22a1%22%3A%221.1%22%2C%22a2%22%3A1733494942646%2C%22a3%22%3A%227x3059v88y925u1518zw20wwzu1wx6v58060x9w8zv4979589771uwv2%22%2C%22a5%22%3A%22LRhx15AvGgVlS5SlzxNNUI%3D%3D%22%2C%22a6%22%3A%22hs1.4aOG4x69iuIGtADfqn9IKcZRvJhUHva43kN8xuj0PhWvWTKjeWclwe%2FfN2xZAm9g8cuh%2BEHA%2BMUMZdFqoPwoDCQ%3D%3D%22%2C%22x0%22%3A4%2C%22d1%22%3A%2275280a98d80370c167ae5b3bad2b7a55%22%7D
referer:https://waimaieapp.meituan.com/igate/bizdata/flowrate?_source=PC&token=0htOuf1eAVTbQaMBK3QAX2GtljWt2JYI6sDdm24Cj-l0*&acctId=179220072&wmPoiId=20089767&region_id=1000510100&device_uuid=!ed40773c-fe5d-4bfb-96a3-aac5882b497f&bsid=KJ4Sv2DmfEPAw-Ju_m02IVlkarO7CTZDRuPty8q4qWgPg4dG8ASZceJzvQsvsauir1Se296s4mbrBJh7BxBTeQ&appType=3&fromPoiChange=false&userId=&topOrigin=https%253A%252F%252Fwaimaie.meituan.com
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36
{
token: 0htOuf1eAVTbQaMBK3QAX2GtljWt2JYI6sDdm24Cj-l0*
wmPoiId: 20089767
acctId: 179220072
appType: 3
durationType: 1
dt: 
ignoreSetRouterProxy: true
yodaReady: h5
csecplatform: 4
csecversion: 2.4.0
mtgsig: {"a1":"1.1","a2":1733494942646,"a3":"7x3059v88y925u1518zw20wwzu1wx6v58060x9w8zv4979589771uwv2","a5":"LRhx15AvGgVlS5SlzxNNUI==","a6":"hs1.4aOG4x69iuIGtADfqn9IKcZRvJhUHva43kN8xuj0PhWvWTKjeWclwe/fN2xZAm9g8cuh+EHA+MUMZdFqoPwoDCQ==","x0":4,"d1":"75280a98d80370c167ae5b3bad2b7a55"}
}

"""