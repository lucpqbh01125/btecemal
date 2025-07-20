<template>
  <div>
    <b-overlay :show="loading" rounded="sm">
      <b-table
        :items="emails"
        :fields="fields"
        responsive
        striped
        hover
        :busy="loading"
        class="align-middle"
        sort-by="received_time"
        sort-desc
      >
        <!-- Phần template cho các cột -->
        <template #cell(title)="data">
          <span :class="{'font-weight-bold': isNew(data.item)}">
            {{ data.item.title }}
          </span>
        </template>

        <template #cell(from_email)="data">
          <span class="text-nowrap">{{ data.item.from_email }}</span>
        </template>

        <template #cell(received_time)="data">
          <span class="text-nowrap">{{ formatDate(data.item.received_time) }}</span>
        </template>

        <template #cell(category)="data">
          <b-badge :variant="getCategoryVariant(data.item.category)" pill>
            {{ getCategoryName(data.item.category) }}
          </b-badge>
          <b-badge v-if="data.item.level" :variant="getLevelVariant(data.item.level)" class="ml-1">
            {{ getLevelName(data.item.level) }}
          </b-badge>
        </template>

        <template #cell(confidence_score)="data">
          <template v-if="data.item.confidence_score > 0">
            <b-progress
              :value="data.item.confidence_score"
              :variant="getScoreVariant(data.item.confidence_score)"
              height="5px"
              class="mt-1"
              :max="100"
            ></b-progress>
            {{ Math.round(data.item.confidence_score) }}%
          </template>
          <span v-else>-</span>
        </template>

        <template #cell(actions)="data">
          <b-button size="sm" variant="primary" @click="viewEmail(data.item)" class="mr-1">
            <b-icon-eye></b-icon-eye> Xem
          </b-button>
          <b-button size="sm" variant="success" @click="analyzeEmail(data.item)">
            <b-icon-lightning-fill></b-icon-lightning-fill> Phân tích
          </b-button>
        </template>

        <template #empty>
          <div class="text-center p-4">
            <b-icon-inbox-fill font-scale="3"></b-icon-inbox-fill>
            <p class="mt-3">Không tìm thấy email nào</p>
          </div>
        </template>
      </b-table>

      <div class="d-flex justify-content-between align-items-center">
        <b-pagination
          v-model="currentPage"
          :total-rows="totalRows"
          :per-page="perPage"
          aria-controls="emails-table"
          align="center"
          first-number
          last-number
          prev-class="prev-item"
          next-class="next-item"
          class="mb-0"
        ></b-pagination>
        
        <div>
          <b-button variant="outline-secondary" size="sm" @click="refreshEmails">
            <b-icon-arrow-clockwise></b-icon-arrow-clockwise> Làm mới
          </b-button>
        </div>
      </div>
    </b-overlay>

    <!-- Modal hiển thị chi tiết email -->
    <b-modal 
      v-model="showEmailModal" 
      size="lg" 
      :title="`Email: ${selectedEmail.title || ''}`"
      scrollable
      hide-footer
    >
      <template v-if="selectedEmail.id">
        <b-card class="mb-3">
          <b-card-text>
            <strong>Người gửi:</strong> {{ selectedEmail.from_email }}<br>
            <strong>Người nhận:</strong> {{ selectedEmail.to_email }}<br>
            <strong>Thời gian:</strong> {{ formatDate(selectedEmail.received_time) }}<br>
            <strong>Phân loại:</strong> 
            <b-badge :variant="getCategoryVariant(selectedEmail.category)" pill>
              {{ getCategoryName(selectedEmail.category) }}
            </b-badge>
            <b-badge v-if="selectedEmail.level" :variant="getLevelVariant(selectedEmail.level)" class="ml-1">
              {{ getLevelName(selectedEmail.level) }}
            </b-badge>
          </b-card-text>
          
          <b-card-text v-if="selectedEmail.suspicious_indicators">
            <div class="mt-2">
              <strong>Mức độ nguy hiểm:</strong>
              <b-progress 
                :value="selectedEmail.confidence_score" 
                :variant="getScoreVariant(selectedEmail.confidence_score)" 
                height="10px"
                class="mt-1 mb-2"
              ></b-progress>
              <div class="text-right">{{ Math.round(selectedEmail.confidence_score) }}%</div>
            </div>

            <div v-if="selectedEmail.suspicious_indicators.reasons && selectedEmail.suspicious_indicators.reasons.length > 0" class="mt-3">
              <strong>Các lý do:</strong>
              <ul class="mt-1 mb-0">
                <li v-for="(reason, index) in selectedEmail.suspicious_indicators.reasons" :key="index">
                  {{ reason }}
                </li>
              </ul>
            </div>

            <div v-if="selectedEmail.recommendation" class="alert alert-info mt-3">
              <strong>Khuyến nghị:</strong> {{ selectedEmail.recommendation }}
            </div>
          </b-card-text>
        </b-card>

        <b-card header="Nội dung email" class="email-content">
          <pre class="mb-0">{{ selectedEmail.content }}</pre>
        </b-card>
      </template>
      <template v-else>
        <p>Không có dữ liệu để hiển thị</p>
      </template>
    </b-modal>

    <!-- Modal hiển thị kết quả phân tích -->
    <b-modal
      v-model="showAnalysisResultModal"
      size="lg"
      title="Kết quả phân tích email"
      scrollable
      hide-footer
    >
      <div v-if="analysisResult">
        <b-alert variant="success" show>
          <strong>Phân tích thành công!</strong>
        </b-alert>
        
        <b-card class="mb-3">
          <b-card-text>
            <strong>Phân loại:</strong> 
            <b-badge :variant="getCategoryVariant(analysisResult.data.category)" pill>
              {{ getCategoryName(analysisResult.data.category) }}
            </b-badge>
            <b-badge v-if="analysisResult.data.level" :variant="getLevelVariant(analysisResult.data.level)" class="ml-1">
              {{ getLevelName(analysisResult.data.level) }}
            </b-badge>
          </b-card-text>
          
          <b-card-text v-if="analysisResult.data.suspicious_indicators">
            <div class="mt-2">
              <strong>Mức độ nguy hiểm:</strong>
              <b-progress 
                :value="analysisResult.data.confidence_score" 
                :variant="getScoreVariant(analysisResult.data.confidence_score)" 
                height="10px"
                class="mt-1 mb-2"
              ></b-progress>
              <div class="text-right">{{ Math.round(analysisResult.data.confidence_score) }}%</div>
            </div>

            <div v-if="analysisResult.data.suspicious_indicators.reasons && analysisResult.data.suspicious_indicators.reasons.length > 0" class="mt-3">
              <strong>Các lý do:</strong>
              <ul class="mt-1 mb-0">
                <li v-for="(reason, index) in analysisResult.data.suspicious_indicators.reasons" :key="index">
                  {{ reason }}
                </li>
              </ul>
            </div>

            <div v-if="analysisResult.data.recommendation" class="alert alert-info mt-3">
              <strong>Khuyến nghị:</strong> {{ analysisResult.data.recommendation }}
            </div>
          </b-card-text>
        </b-card>
        
        <div class="text-right">
          <b-button @click="showAnalysisResultModal = false" variant="secondary">Đóng</b-button>
        </div>
      </div>
      <div v-else class="text-center">
        <p>Không có kết quả phân tích</p>
      </div>
    </b-modal>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex';
import { 
  BIconEye, 
  BIconLightningFill, 
  BIconArrowClockwise, 
  BIconInboxFill 
} from 'bootstrap-vue';

export default {
  name: 'EmailList',
  components: {
    BIconEye,
    BIconLightningFill,
    BIconArrowClockwise,
    BIconInboxFill
  },
  props: {
    selectedCategory: {
      type: String,
      default: 'all'
    }
  },
  data() {
    return {
      currentPage: 1,
      perPage: 10,
      totalRows: 0,
      showEmailModal: false,
      selectedEmail: {},
      showAnalysisResultModal: false,  // Thêm biến cho modal kết quả phân tích
      analysisResult: null,            // Thêm biến để lưu kết quả phân tích
      fields: [
        { key: 'title', label: 'Tiêu đề', sortable: true },
        { key: 'from_email', label: 'Người gửi', sortable: true },
        { key: 'received_time', label: 'Thời gian nhận', sortable: true },
        { key: 'category', label: 'Phân loại', sortable: true },
        { key: 'confidence_score', label: 'Độ tin cậy', sortable: true },
        { key: 'actions', label: 'Thao tác' }
      ]
    };
  },
  computed: {
    ...mapState({
      emails: state => state.emails,
      loading: state => state.loading
    }),
  },
  watch: {
    currentPage() {
      this.loadEmails();
    },
    selectedCategory() {
      this.currentPage = 1;
      this.loadEmails();
    }
  },
  created() {
    this.loadEmails();
  },
  methods: {
    ...mapActions(['fetchEmails', 'analyzeSingleEmail']),
    
    loadEmails() {
      const offset = (this.currentPage - 1) * this.perPage;
      const category = this.selectedCategory !== 'all' ? this.selectedCategory : null;
      
      this.fetchEmails({ 
        limit: this.perPage, 
        offset, 
        category 
      }).then(() => {
        this.totalRows = this.emails.length < this.perPage 
          ? (this.currentPage - 1) * this.perPage + this.emails.length 
          : this.currentPage * this.perPage + 10; // Ước lượng
      });
    },
    
    refreshEmails() {
      this.loadEmails();
    },
    
    viewEmail(email) {
      this.selectedEmail = { ...email };
      this.showEmailModal = true;
    },
    
    async analyzeEmail(email) {
      try {
        const result = await this.analyzeSingleEmail({
          id: email.id,
          title: email.title,
          content: email.content,
          sender: email.from_email
        });
        
        if (result && result.success) {
          // Lưu kết quả phân tích và hiển thị modal
          this.analysisResult = result;
          this.showAnalysisResultModal = true;
          
          // Làm mới danh sách để hiển thị kết quả
          this.refreshEmails();
        } else {
          // Hiển thị thông báo lỗi
          this.$bvToast.toast(result.message || 'Phân tích thất bại', {
            title: 'Lỗi',
            variant: 'danger',
            solid: true
          });
        }
      } catch (error) {
        console.error('Lỗi khi phân tích email:', error);
        this.$bvToast.toast('Đã xảy ra lỗi khi phân tích email', {
          title: 'Lỗi',
          variant: 'danger',
          solid: true
        });
      }
    },
    
    formatDate(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      return new Intl.DateTimeFormat('vi-VN', {
        year: 'numeric', 
        month: '2-digit', 
        day: '2-digit',
        hour: '2-digit', 
        minute: '2-digit'
      }).format(date);
    },
    
    isNew(email) {
      if (!email.created_at) return false;
      const created = new Date(email.created_at);
      const now = new Date();
      const hoursDiff = (now - created) / (1000 * 60 * 60);
      return hoursDiff < 24;
    },
    
    getCategoryName(category) {
      const categories = {
        'safe': 'An toàn',
        'suspicious': 'Đáng ngờ',
        'spam': 'Spam',
        'phishing': 'Lừa đảo',
        'unknown': 'Chưa phân loại'
      };
      return categories[category] || category;
    },
    
    getCategoryVariant(category) {
      const variants = {
        'safe': 'success',
        'suspicious': 'warning',
        'spam': 'secondary',
        'phishing': 'danger',
        'unknown': 'info'
      };
      return variants[category] || 'light';
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
.email-content pre {
  white-space: pre-wrap;
  word-wrap: break-word;
  max-height: 300px;
  overflow-y: auto;
}

.prev-item,
.next-item {
  font-size: 0.9rem;
}

/* Hiệu ứng cho hover trên bảng */
.table-hover tbody tr:hover {
  background-color: rgba(0, 123, 255, 0.075);
}
</style> 