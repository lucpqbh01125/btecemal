<template>
  <div>
    <h1 class="mb-4">
      Tổng quan hệ thống
      <span class="float-right">
        <b-form-checkbox v-model="autoRefresh" switch size="lg" class="mt-2">
          <span :class="{'text-success': autoRefresh}">Tự động cập nhật</span>
          <b-badge v-if="autoRefresh" variant="light" class="ml-1">{{ autoRefreshCountdown }}s</b-badge>
        </b-form-checkbox>
      </span>
    </h1>

    <b-alert 
      :show="showSuccessAlert" 
      variant="success" 
      dismissible 
      class="position-fixed"
      style="top: 10px; right: 10px; z-index: 9999; width: 400px;"
    >
      {{ successMessage }}
    </b-alert>

    <b-row>
      <b-col cols="12" md="8">
        <b-card title="Thống kê email" class="mb-4">
          <b-overlay :show="loading" rounded="sm">
            <email-stats-chart />
          </b-overlay>
        </b-card>
      </b-col>

      <b-col cols="12" md="4">
        <b-card title="Tóm tắt (hãy thao tác lựa chọn để lọc được email nghi ngờ)" class="mb-4">
          <b-list-group flush>
            <b-list-group-item>
              <div class="d-flex justify-content-between align-items-center">
                <span>Tổng số email</span>
                <b-badge variant="primary">{{ stats.totalEmails }}</b-badge>
              </div>
            </b-list-group-item>
            <b-list-group-item 
              @click="filterEmailsByCategory('safe')"
              class="clickable-item"
              :class="{'active-filter': activeCategory === 'safe'}"
            >
              <div class="d-flex justify-content-between align-items-center">
                <span class="text-success">Email an toàn</span>
                <b-badge variant="success">{{ stats.categories.safe.count }}</b-badge>
              </div>
            </b-list-group-item>
            <b-list-group-item 
              @click="filterEmailsByCategory('suspicious')"
              class="clickable-item"
              :class="{'active-filter': activeCategory === 'suspicious'}"
            >
              <div class="d-flex justify-content-between align-items-center">
                <span class="text-warning">Email đáng ngờ</span>
                <b-badge variant="warning">{{ stats.categories.suspicious.count }}</b-badge>
              </div>
            </b-list-group-item>
            <b-list-group-item 
              @click="filterEmailsByCategory('spam')"
              class="clickable-item"
              :class="{'active-filter': activeCategory === 'spam'}"
            >
              <div class="d-flex justify-content-between align-items-center">
                <span class="text-secondary">Email spam</span>
                <b-badge variant="secondary">{{ stats.categories.spam.count }}</b-badge>
              </div>
            </b-list-group-item>
            <b-list-group-item 
              @click="filterEmailsByCategory('phishing')"
              class="clickable-item"
              :class="{'active-filter': activeCategory === 'phishing'}"
            >
              <div class="d-flex justify-content-between align-items-center">
                <span class="text-danger">Email lừa đảo</span>
                <b-badge variant="danger">{{ stats.categories.phishing.count }}</b-badge>
              </div>
            </b-list-group-item>
            <b-list-group-item 
              @click="filterEmailsByCategory('unknown')"
              class="clickable-item"
              :class="{'active-filter': activeCategory === 'unknown'}"
            >
              <div class="d-flex justify-content-between align-items-center">
                <span class="text-info">Email chưa phân loại</span>
                <b-badge variant="info">{{ stats.categories.unknown.count }}</b-badge>
              </div>
            </b-list-group-item>
          </b-list-group>

          <div class="mt-3">
            <!-- Button đã ẩn -->
          </div>
        </b-card>
      </b-col>
    </b-row>

    <h2 class="mt-4 mb-3">
      Email gần đây
      <span v-if="activeCategory !== 'all'" class="ml-2">
        <b-badge :variant="getCategoryVariant(activeCategory)">
          {{ getCategoryName(activeCategory) }}
        </b-badge>
        <b-button size="sm" variant="outline-secondary" class="ml-2" @click="filterEmailsByCategory('all')">
          Xóa bộ lọc
        </b-button>
      </span>
    </h2>

    <b-alert :show="!!error" variant="danger">{{ error }}</b-alert>
    
    <email-list ref="emailList" :selectedCategory="activeCategory" />
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex';
import EmailStatsChart from '@/components/EmailStatsChart.vue';
import EmailList from '@/components/EmailList.vue';

export default {
  name: 'DashboardView',
  components: {
    EmailStatsChart,
    EmailList
  },
  data() {
    return {
      showSuccessAlert: false,
      successMessage: '',
      autoRefresh: false,
      autoRefreshInterval: null,
      autoRefreshCountdown: 30,
      autoRefreshTime: 30000, // 30 giây
      activeCategory: 'all' // Danh mục hiện tại đang được lọc
    };
  },
  computed: {
    ...mapState(['stats', 'loading', 'processingBatch', 'error'])
  },
  watch: {
    autoRefresh(newValue) {
      if (newValue) {
        this.startAutoRefresh();
      } else {
        this.stopAutoRefresh();
      }
    }
  },
  created() {
    // Tải dữ liệu ban đầu
    this.refreshData();
  },
  beforeDestroy() {
    // Hủy timer trước khi component bị hủy
    this.stopAutoRefresh();
  },
  methods: {
    ...mapActions(['fetchStats', 'fetchEmails', 'analyzeBatch']),
    
    async refreshData() {
      // Tải thống kê và dữ liệu email
      await this.fetchStats();
    },
    
    startAutoRefresh() {
      this.autoRefreshCountdown = this.autoRefreshTime / 1000;
      
      // Tạo interval cho đếm ngược
      const countdownInterval = setInterval(() => {
        this.autoRefreshCountdown--;
        if (this.autoRefreshCountdown <= 0) {
          this.autoRefreshCountdown = this.autoRefreshTime / 1000;
        }
      }, 1000);
      
      // Tạo interval cho refresh dữ liệu
      this.autoRefreshInterval = setInterval(() => {
        this.refreshData();
      }, this.autoRefreshTime);
      
      // Lưu interval đếm ngược để hủy sau này
      this._countdownInterval = countdownInterval;
    },
    
    stopAutoRefresh() {
      clearInterval(this.autoRefreshInterval);
      clearInterval(this._countdownInterval);
      this.autoRefreshInterval = null;
    },
    
    async batchAnalyze(limit) {
      try {
        const result = await this.analyzeBatch(limit);
        
        if (result && result.success) {
          this.showSuccessAlert = true;
          this.successMessage = result.message;
          
          // Tự động đóng alert sau 5 giây
          setTimeout(() => {
            this.showSuccessAlert = false;
          }, 5000);
        }
      } catch (error) {
        console.error("Lỗi phân tích email:", error);
        this.successMessage = `Lỗi: ${error.message || 'Không thể phân loại email'}`;
        this.showSuccessAlert = true;
      }
    },
    
    filterEmailsByCategory(category) {
      this.activeCategory = category;
    },
    
    getCategoryName(category) {
      const categories = {
        'safe': 'An toàn',
        'suspicious': 'Đáng ngờ',
        'spam': 'Spam',
        'phishing': 'Lừa đảo',
        'unknown': 'Chưa phân loại',
        'all': 'Tất cả'
      };
      return categories[category] || category;
    },
    
    getCategoryVariant(category) {
      const variants = {
        'safe': 'success',
        'suspicious': 'warning',
        'spam': 'secondary',
        'phishing': 'danger',
        'unknown': 'info',
        'all': 'primary'
      };
      return variants[category] || 'light';
    }
  }
};
</script>

<style scoped>
.clickable-item {
  cursor: pointer;
}

.active-filter {
  background-color: rgba(0, 123, 255, 0.1);
  font-weight: bold;
}
</style> 