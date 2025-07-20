import apiClient from './http';

/**
 * API liên quan đến email và phân tích
 */
export default {
  /**
   * Lấy thống kê về email
   */
  getStats() {
    return apiClient.get('/emails/stats');
  },

  /**
   * Lấy danh sách email với các tùy chọn filter
   * @param {Object} options - Các tùy chọn
   * @param {number} options.limit - Số lượng email tối đa
   * @param {number} options.offset - Vị trí bắt đầu
   * @param {string} options.category - Lọc theo loại email
   */
  getEmails({ limit = 50, offset = 0, category = null } = {}) {
    let url = `/emails?limit=${limit}&offset=${offset}`;
    if (category && category !== 'all') {
      url += `&category=${category}`;
    }
    return apiClient.get(url);
  },

  /**
   * Phân tích một email
   * @param {Object} data - Thông tin email cần phân tích
   * @param {string} data.title - Tiêu đề email
   * @param {string} data.content - Nội dung email
   * @param {string} data.sender - Email người gửi
   */
  analyzeEmail(data) {
    return apiClient.post('/emails/analyze', data);
  },

  /**
   * Phân tích hàng loạt email chưa phân loại
   * @param {number} limit - Số lượng email tối đa cần phân tích
   */
  analyzeBatch(limit) {
    let url = '/emails/analyze-batch';
    if (limit !== undefined && limit !== -1) {
      url += `?limit=${limit}`;
    }
    return apiClient.post(url);
  }
}; 