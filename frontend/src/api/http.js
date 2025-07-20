import axios from 'axios';

// Lấy base URL từ biến môi trường hoặc dùng giá trị mặc định
const API_URL = process.env.VUE_APP_API_URL || 'http://localhost:8000/api';

console.log('API URL:', API_URL); // Debug: Hiển thị URL đang được sử dụng

// Tạo instance axios với các cấu hình mặc định
const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },
  timeout: 15000 // 15 giây timeout
});

// Interceptor cho request
apiClient.interceptors.request.use(
  (config) => {
    // Thêm logic xử lý request nếu cần
    console.log(`Request: ${config.method.toUpperCase()} ${config.baseURL}${config.url}`);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor cho response
apiClient.interceptors.response.use(
  (response) => {
    console.log(`Response from ${response.config.url}: Status ${response.status}`);
    return response;
  },
  (error) => {
    // Xử lý các loại lỗi
    if (error.response) {
      // Lỗi server trả về
      console.error('API Error:', error.response.data);
    } else if (error.request) {
      // Không nhận được response
      console.error('Network Error:', error.request);
    } else {
      // Lỗi trong quá trình setup request
      console.error('Request Error:', error.message);
    }
    
    return Promise.reject(error);
  }
);

export default apiClient; 