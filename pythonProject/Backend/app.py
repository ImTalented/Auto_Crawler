from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from spider_handler import start_crawler
import requests
import logging


app = Flask(__name__)
CORS(app)

# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 数据模型
class UserCookie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    cookie = db.Column(db.Text, nullable=False)


# 模拟登录的临时存储,防止第二步验证时，没有session导致用户对话丢失
login_sessions = {}

# 第一步：提交用户名和密码
@app.route('/api/add_user_step1', methods=['POST'])
def add_user_step1():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # 模拟登录请求
    session = requests.Session()
    login_url = "https://waimaie.meituan.com/login"  # 示例登录 URL
    payload = {"username": username, "password": password}
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = session.post(login_url, data=payload, headers=headers)
        if "验证码" in response.text:  # 判断是否需要验证码
            user_id = len(login_sessions) + 1
            login_sessions[user_id] = session
            return jsonify({"requires_captcha": True, "user_id": user_id})
        else:
            cookie_dict = session.cookies.get_dict()
            cookie_str = "; ".join([f"{k}={v}" for k, v in cookie_dict.items()])

            # 存储到数据库
            new_user = UserCookie(username=username, cookie=cookie_str)
            db.session.add(new_user)
            db.session.commit()

            return jsonify({"message": "用户添加成功"})
    except Exception as e:
        return jsonify({"error": f"登录失败: {str(e)}"}), 500

# 第二步：提交验证码完成登录
@app.route('/api/add_user_step2', methods=['POST'])
def add_user_step2():
    data = request.json
    user_id = data.get('user_id')
    captcha = data.get('captcha')

    session = login_sessions.get(user_id)
    if not session:
        return jsonify({"error": "无效的用户 ID"}), 404

    try:
        # 提交验证码
        captcha_url = "https://waimaie.meituan.com/captcha"  # 示例验证码提交 URL
        response = session.post(captcha_url, data={"captcha": captcha})
        if response.status_code == 200:
            cookie_dict = session.cookies.get_dict()
            cookie_str = "; ".join([f"{k}={v}" for k, v in cookie_dict.items()])

            # 存储到数据库
            new_user = UserCookie(username="unknown", cookie=cookie_str)
            db.session.add(new_user)
            db.session.commit()

            del login_sessions[user_id]
            return jsonify({"message": "验证码提交成功，用户添加完成"})
        else:
            return jsonify({"error": "验证码错误或提交失败"}), 400
    except Exception as e:
        return jsonify({"error": f"提交验证码失败: {str(e)}"}), 500




# 删除用户
@app.route('/api/delete_user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = UserCookie.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"})
    return jsonify({"error": "User not found"}), 404

#检查用户cookie
@app.route('/api/check_cookie/<int:user_id>', methods=['GET'])
def check_cookie(user_id):
    user = UserCookie.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # 用 cookie 访问外网验证
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/json",
    }

    #将cookie的字符串格式转换为字典格式
    cookie_dict = dict(item.split('=') for item in user.cookie.split('; '))

    try:
        response = requests.get("https://waimaie.meituan.com/", headers=headers, cookies=cookie_dict)
        if response.status_code == 200:
            return jsonify({"status": "valid"})
        else:
            return jsonify({"status": "invalid"})
    except Exception as e:
        return jsonify({"error": f"Failed to check cookie: {str(e)}"}), 500

#获取原始数据库已有用户(网页启动时，自动提取数据库已有数据)
@app.route('/api/users', methods=['GET'])
def get_users():
    users = UserCookie.query.all()
    user_list = [{"id": user.id, "username": user.username, "cookie": user.cookie} for user in users]
    return jsonify(user_list)


#执行爬虫，并存入本地csv或excel
@app.route('/api/run_spider/<int:user_id>', methods=['POST'])
def run_spider(user_id):
    user = UserCookie.query.get(user_id)
    cookie_dict = dict(item.split('=') for item in user.cookie.split('; '))
    if not user:
        return jsonify({"error": "User not found"}), 404
    # 发送请求到爬虫服务
    start_crawler(cookie_dict)
    return jsonify({"message": "Succeed to crawl"})




if __name__ == '__main__':
    #初始化数据库
    with app.app_context():  # 手动进入 Flask 应用上下文
        db.create_all()
    app.run(debug=True, port=5000)
