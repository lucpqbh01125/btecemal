import Vue from 'vue'
import VueRouter from 'vue-router'
import Dashboard from '../views/Dashboard.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard,
    meta: { title: 'Dashboard' }
  },
  {
    path: '/check-email',
    name: 'CheckEmail',
    // Lazy-load the component
    component: () => import('../views/CheckEmail.vue'),
    meta: { title: 'Kiểm tra email' }
  },
  {
    path: '/education',
    name: 'Education',
    component: () => import('../views/Education.vue'),
    meta: { title: 'Hướng dẫn phòng tránh' }
  },
  {
    path: '/report',
    name: 'Report',
    component: () => import('../views/Report.vue'),
    meta: { title: 'Báo cáo phân tích' }
  },
  {
    path: '*',
    name: 'NotFound',
    component: () => import('../views/NotFound.vue'),
    meta: { title: 'Trang không tồn tại' }
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

// Thay đổi tiêu đề trang dựa trên route
router.beforeEach((to, from, next) => {
  document.title = to.meta.title ? `${to.meta.title} | Email Analyzer` : 'Email Analyzer'
  next()
})

export default router 