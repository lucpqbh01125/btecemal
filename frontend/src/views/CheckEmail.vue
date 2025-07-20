<template>
  <div>
    <h1 class="mb-4">Kiểm tra email</h1>
    <p class="mb-4">
      Nhập thông tin email cần kiểm tra để xác định mức độ nguy hiểm và phân loại.
    </p>
    
    <b-card class="mb-4">
      <b-form @submit.prevent="analyzeEmail">
        <b-form-group
          label="Tiêu đề email:"
          label-for="title"
          description="Nhập chính xác tiêu đề của email."
        >
          <b-form-input
            id="title"
            v-model="emailForm.title"
            placeholder="Nhập tiêu đề email"
            required
          ></b-form-input>
        </b-form-group>

        <b-form-group
          label="Email người gửi:"
          label-for="sender"
          description="Nhập địa chỉ email của người gửi."
        >
          <b-form-input
            id="sender"
            v-model="emailForm.sender"
            placeholder="example@domain.com"
            required
          ></b-form-input>
        </b-form-group>

        <b-form-group
          label="Nội dung email:"
          label-for="content"
          description="Sao chép và dán toàn bộ nội dung email vào đây."
        >
          <b-form-textarea
            id="content"
            v-model="emailForm.content"
            placeholder="Nhập nội dung email..."
            rows="8"
            max-rows="16"
            required
          ></b-form-textarea>
        </b-form-group>

        <div class="d-flex">
          <b-button type="submit" variant="primary" class="mr-2" :disabled="analyzing">
            <b-spinner small v-if="analyzing" class="mr-1"></b-spinner>
            {{ analyzing ? 'Đang phân tích...' : 'Phân tích email' }}
          </b-button>
          <b-button type="reset" variant="secondary" @click="resetForm">
            Xóa thông tin
          </b-button>
        </div>
      </b-form>
    </b-card>

    <!-- Kết quả phân tích -->
    <b-card v-if="result" class="mb-4" :title="`Kết quả phân tích: ${getCategoryName(result.category)}`">
      <b-alert show variant="info" class="mb-4">
        <strong>Đánh giá: </strong> {{ result.recommendation }}
      </b-alert>
      
      <div class="mb-3">
        <strong>Mức độ tin cậy:</strong>
        <b-progress 
          :value="result.confidence_score" 
          :variant="getScoreVariant(result.confidence_score)"
          class="mt-2" 
          height="10px"
          show-value
          :max="100"
        ></b-progress>
      </div>

      <div class="mb-3">
        <strong>Mức độ nguy hiểm:</strong>
        <b-badge :variant="getLevelVariant(result.level)" class="ml-2">{{ getLevelName(result.level) }}</b-badge>
      </div>
      
      <div v-if="result.suspicious_indicators && result.suspicious_indicators.reasons" class="mb-3">
        <strong>Lý do:</strong>
        <b-list-group class="mt-2">
          <b-list-group-item v-for="(reason, index) in result.suspicious_indicators.reasons" :key="index">
            {{ reason }}
          </b-list-group-item>
        </b-list-group>
      </div>
    </b-card>
    
    <b-alert 
      v-if="error" 
      show
      variant="danger"
      class="mb-4"
      dismissible
      @dismissed="error = ''"
    >
      {{ error }}
    </b-alert>
    
    <b-card class="mb-4">
      <h4 class="mb-3">Hướng dẫn kiểm tra email</h4>
      <ol>
        <li>Sao chép tiêu đề email vào trường "Tiêu đề email".</li>
        <li>Nhập địa chỉ email của người gửi vào trường "Email người gửi".</li>
        <li>Sao chép nội dung email vào trường "Nội dung email".</li>
        <li>Nhấn nút "Phân tích email" để bắt đầu quá trình phân tích.</li>
      </ol>
      <p>
        Hệ thống sẽ phân tích và cho biết email có phải là email lừa đảo (phishing), 
        thư rác (spam), đáng ngờ, hay an toàn, cùng với các chỉ số và lý do cụ thể.
      </p>
    </b-card>
  </div>
</template>

<script>
import { mapActions } from 'vuex';

export default {
  name: 'CheckEmail',
  data() {
    return {
      emailForm: {
        title: '',
        sender: '',
        content: ''
      },
      result: null,
      analyzing: false,
      error: ''
    };
  },
  methods: {
    ...mapActions(['analyzeSingleEmail']),
    
    async analyzeEmail() {
      this.analyzing = true;
      this.error = '';
      this.result = null;
      
      try {
        const response = await this.analyzeSingleEmail({
          title: this.emailForm.title,
          sender: this.emailForm.sender,
          content: this.emailForm.content
        });
        
        if (response.success && response.data) {
          this.result = response.data;
        } else {
          this.error = response.message || 'Không thể phân tích email. Vui lòng thử lại.';
        }
      } catch (error) {
        console.error('Lỗi khi phân tích email:', error);
        this.error = 'Có lỗi xảy ra. Vui lòng thử lại sau.';
      } finally {
        this.analyzing = false;
      }
    },
    
    resetForm() {
      this.emailForm = {
        title: '',
        sender: '',
        content: ''
      };
      this.result = null;
      this.error = '';
    },
    
    getCategoryName(category) {
      const categories = {
        'safe': 'An toàn',
        'suspicious': 'Đáng ngờ',
        'spam': 'Thư rác',
        'phishing': 'Lừa đảo',
        'unknown': 'Chưa xác định'
      };
      return categories[category] || category;
    },
    
    getLevelName(level) {
      const levels = {
        'low': 'Thấp',
        'medium': 'Trung bình',
        'high': 'Cao',
        'critical': 'Nghiêm trọng'
      };
      return levels[level] || level;
    },
    
    getLevelVariant(level) {
      const variants = {
        'low': 'info',
        'medium': 'warning',
        'high': 'danger',
        'critical': 'dark'
      };
      return variants[level] || 'light';
    },
    
    getScoreVariant(score) {
      if (score < 30) return 'success';
      if (score < 60) return 'warning';
      if (score < 80) return 'danger';
      return 'dark';
    }
  }
};
</script>

<style scoped>
.card {
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
}

.progress {
  height: 0.75rem;
  border-radius: 0.5rem;
}
</style> 