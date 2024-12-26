import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5000/api',
});

export const deleteUser = (id) => api.delete(`/delete_user/${id}`);
export const checkCookie = (id) => api.get(`/check_cookie/${id}`);
// 执行爬虫任务
export const runSpider = (id) => api.post(`/run_spider/${id}`);
// 获取用户列表
export const fetchUsers = () => api.get('/users');
// 检查 Cookie 状态
export const checkCookie = (id) => api.get(`/check_cookie/${id}`);

export const add1 = (temp) => api.post('/add_user_step1',temp);
// 检查 Cookie 状态
export const add2 = (temp) => api.post(`/add_user_step2`,temp);