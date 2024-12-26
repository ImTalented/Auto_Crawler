<template>
  <div>
    <h2>用户管理</h2>
    <button @click="showAddUserForm">添加用户</button>
    <ul>
      <li v-for="user in users" :key="user.id">
        {{ user.username }} - {{ user.cookie }}
        <button @click="checkCookie(user.id)">检查 Cookie</button>
        <button @click="runSpider(user.id)">执行爬虫</button>
        <button @click="deleteUser(user.id)">删除</button>
      </li>
    </ul>

    <!-- 添加用户表单 -->
    <div v-if="showForm" class="form-popup">
      <h3>添加用户</h3>
      <input v-model="formData.username" placeholder="用户名" />
      <input v-model="formData.password" type="password" placeholder="密码" />
      <button @click="submitUserInfo">提交</button>
      <button @click="closeForm">取消</button>
    </div>

    <!-- 验证码输入框 -->
    <div v-if="showCaptcha" class="form-popup">
      <h3>请输入验证码</h3>
      <input v-model="captcha" placeholder="验证码" />
      <button @click="submitCaptcha">提交验证码</button>
      <button @click="closeCaptcha">取消</button>
    </div>

  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      users: [], // 用户列表
      showForm: false, // 是否显示添加用户表单
      showCaptcha: false, // 是否显示验证码输入框
      formData: { username: '', password: '' }, // 表单数据
      captcha: '', // 验证码
      currentUserId: null, // 当前处理的用户 ID
    };
  },
  methods: {
    // 显示添加用户表单
    showAddUserForm() {
      this.showForm = true;
    },
    closeForm() {
      this.showForm = false;
      this.formData = { username: '', password: '' };
    },

    // 提交用户名和密码到后端
    async submitUserInfo() {
      try {
        const temp = this.formData
        const response = await axios.post('http://localhost:5000/api/add_user_step1', temp);
        if (response.data.requires_captcha) {
          // 如果需要验证码，显示验证码输入框
          this.showCaptcha = true;
          this.currentUserId = response.data.user_id;
          this.closeForm();
        } else {
          alert(response.data.message);
          this.fetchUsers();
        }
      } catch (error) {
        alert('提交失败：' + error.response.data.error);
      }
    },

    closeCaptcha() {
      this.showCaptcha = false;
      this.captcha = '';
      this.currentUserId = null;
    },

    // 提交验证码到后端
    async submitCaptcha() {
      try {
        const temp = {
          user_id: this.currentUserId,
          captcha: this.captcha,
        }
        const response = await axios.post('http://localhost:5000/api/add_user_step2', temp);
        alert(response.data.message);
        this.closeCaptcha();
        this.fetchUsers();
      } catch (error) {
        alert('验证码提交失败：' + error.response.data.error);
      }
    },

    // 检查 Cookie 状态
    async checkCookie(id) {
      const response = await axios.get(`http://localhost:5000/api/check_cookie/${id}`);
      alert(`Cookie 状态: ${response.data.status}`);
    },

    // 执行爬虫任务
    async runSpider(id) {
      try {
        const response = await axios.post(`http://localhost:5000/api/run_spider/${id}`);
        alert(response.data.message || response.data.error);
      } catch (error) {
        alert("爬虫执行失败，请检查后端服务！");
      }
    },

    // 删除用户
    async deleteUser(id) {
      await axios.delete(`http://localhost:5000/api/delete_user/${id}`);
      this.fetchUsers();
    },

    // 获取用户列表（网页启动后，先从后端数据库获取对应user信息（用户名+cookie）
    async fetchUsers() {
      const response = await axios.get("http://localhost:5000/api/users");
      this.users = response.data;
    },
  },
  mounted() {
    this.fetchUsers();
  },
};
</script>



































<!--<template>-->
<!--  <div>-->
<!--    <h2>用户管理</h2>-->
<!--    <button @click="addUser">添加用户</button>-->
<!--    <ul>-->
<!--      <li v-for="user in users" :key="user.id">-->
<!--        {{ user.username }} - {{ user.cookie }}-->
<!--        <button @click="deleteUser(user.id)">删除</button>-->
<!--      </li>-->
<!--    </ul>-->
<!--  </div>-->
<!--</template>-->

<!--<script>-->
<!--import axios from 'axios';-->


<!--// 典型的异步脱耦处理，通过后台和前台信息交互，来进行页面刷新-->
<!--export default {-->
<!--  data() {-->
<!--    return {-->
<!--      users: [],-->
<!--    };-->
<!--  },-->
<!--  methods: {-->
<!--    addUser() {-->
<!--      // 打开新窗口登录-->
<!--      const loginWindow = window.open(-->
<!--        "https://waimaie.meituan.com/",-->
<!--        "_blank",-->
<!--        "width=800,height=600"-->
<!--      );-->

<!--      // 监听窗口关闭-->
<!--      const timer = setInterval(() => {-->
<!--        if (loginWindow.closed) {-->
<!--          clearInterval(timer);-->
<!--          // 假设此时已经登录，后端会调用爬虫获取 cookie-->
<!--          this.requestCookie();-->
<!--        }-->
<!--      }, 1000);-->
<!--    },-->
<!--    async requestCookie() {-->
<!--      const username = prompt("请输入用户名：");-->
<!--      if (username) {-->
<!--        const response = await axios.post("http://localhost:5000/api/add_user", {-->
<!--          username,-->
<!--        });-->
<!--        alert(response.data.message || response.data.error);-->
<!--        this.fetchUsers();-->
<!--      }-->
<!--    },-->
<!--    async deleteUser(id) {-->
<!--      await axios.delete(`http://localhost:5000/api/delete_user/${id}`);-->
<!--      this.fetchUsers();-->
<!--    },-->
<!--    async fetchUsers() {-->
<!--      // 示例：刷新用户列表-->
<!--      // 如果后端实现了获取用户列表的 API，则在这里获取-->
<!--      // 典型的异步脱耦处理，通过后台和前台信息交互，来进行页面刷新-->
<!--      console.log("刷新用户列表");-->
<!--    },-->
<!--  },-->
<!--  mounted() {-->
<!--    this.fetchUsers();-->
<!--  },-->
<!--};-->
<!--</script>-->
