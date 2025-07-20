import Vue from 'vue'
import Vuex from 'vuex'
import emailApi from '../api/email'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    emails: [],
    stats: {
      totalEmails: 0,
      categories: {
        safe: { count: 0, percentage: 0 },
        suspicious: { count: 0, percentage: 0 },
        spam: { count: 0, percentage: 0 },
        phishing: { count: 0, percentage: 0 },
        unknown: { count: 0, percentage: 0 }
      },
      recent_trend: []
    },
    loading: false,
    processingBatch: false,
    error: null
  },
  
  mutations: {
    SET_EMAILS(state, emails) {
      state.emails = emails
    },
    
    SET_STATS(state, stats) {
      // Chuyển đổi dữ liệu stats từ API để phù hợp với state
      state.stats = {
        totalEmails: stats.total,
        categories: stats.categories,
        recent_trend: stats.recent_trend || []
      }
    },
    
    SET_LOADING(state, value) {
      state.loading = value
    },
    
    SET_PROCESSING_BATCH(state, value) {
      state.processingBatch = value
    },
    
    SET_ERROR(state, error) {
      state.error = error
    },
    
    UPDATE_EMAIL(state, updatedEmail) {
      const index = state.emails.findIndex(email => email.id === updatedEmail.id)
      if (index !== -1) {
        state.emails.splice(index, 1, updatedEmail)
      }
    }
  },
  
  actions: {
    async fetchStats({ commit }) {
      commit('SET_LOADING', true)
      try {
        const response = await emailApi.getStats()
        commit('SET_STATS', response.data)
      } catch (error) {
        console.error('Error fetching stats:', error)
        commit('SET_ERROR', 'Không thể tải dữ liệu thống kê')
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async fetchEmails({ commit }, options = {}) {
      commit('SET_LOADING', true)
      try {
        const response = await emailApi.getEmails(options)
        commit('SET_EMAILS', response.data)
        return response.data
      } catch (error) {
        console.error('Error fetching emails:', error)
        commit('SET_ERROR', 'Không thể tải dữ liệu email')
        return []
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async analyzeBatch({ commit }, limit) {
      commit('SET_PROCESSING_BATCH', true)
      try {
        const response = await emailApi.analyzeBatch(limit)
        
        // Cập nhật stats sau khi phân tích
        await this.dispatch('fetchStats')
        
        return {
          success: true,
          message: response.data.message
        }
      } catch (error) {
        console.error('Error analyzing batch:', error)
        commit('SET_ERROR', 'Lỗi khi phân tích hàng loạt email')
        return {
          success: false,
          message: error.response?.data?.detail || 'Lỗi khi phân tích hàng loạt email'
        }
      } finally {
        commit('SET_PROCESSING_BATCH', false)
      }
    },
    
    async analyzeSingleEmail(context, data) {
      try {
        const response = await emailApi.analyzeEmail(data)
        
        if (response.data.success && data.id) {
          // Nếu phân tích thành công và có ID, cập nhật dữ liệu
          await this.dispatch('fetchEmails')
          await this.dispatch('fetchStats')
        }
        
        return response.data
      } catch (error) {
        console.error('Error analyzing email:', error)
        return {
          success: false,
          message: error.response?.data?.detail || 'Lỗi khi phân tích email'
        }
      }
    }
  },
  
  getters: {
    emailsByCategory: (state) => (category) => {
      if (!category || category === 'all') {
        return state.emails
      }
      return state.emails.filter(email => email.category === category)
    },
    
    emailsCount: (state) => {
      return state.emails.length
    }
  }
}) 