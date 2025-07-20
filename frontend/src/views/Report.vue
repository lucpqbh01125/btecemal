<template>
  <div>
    <h1 class="mb-4">Báo cáo phân tích email</h1>

    <b-card class="mb-4">
      <b-form-group label="Khoảng thời gian:">
        <b-row>
          <b-col md="5">
            <b-form-datepicker v-model="startDate" placeholder="Từ ngày" :max="endDate || today"></b-form-datepicker>
          </b-col>
          <b-col md="5">
            <b-form-datepicker v-model="endDate" placeholder="Đến ngày" :min="startDate" :max="today"></b-form-datepicker>
          </b-col>
          <b-col md="2">
            <b-button variant="primary" block @click="generateReport" :disabled="loading">
              <b-spinner small v-if="loading"></b-spinner>
              <span v-else>Tạo báo cáo</span>
            </b-button>
          </b-col>
        </b-row>
      </b-form-group>
    </b-card>

    <b-overlay :show="loading" rounded>
      <b-card class="mb-4">
        <h3 class="mb-4">Tổng quan phân tích</h3>
        <b-row>
          <b-col md="6">
            <apexchart 
              type="pie" 
              height="320" 
              :options="pieChartOptions" 
              :series="pieChartSeries"
            ></apexchart>
          </b-col>
          <b-col md="6">
            <div class="stats-summary">
              <h4>Thống kê email trong khoảng thời gian</h4>
              <b-list-group flush>
                <b-list-group-item class="d-flex justify-content-between align-items-center">
                  <span>Tổng số email đã phân tích:</span>
                  <b-badge variant="primary" pill>{{ stats.totalEmails || 0 }}</b-badge>
                </b-list-group-item>
                <b-list-group-item class="d-flex justify-content-between align-items-center">
                  <span class="text-success">Email an toàn:</span>
                  <b-badge variant="success" pill>{{ stats.categories.safe?.count || 0 }}</b-badge>
                </b-list-group-item>
                <b-list-group-item class="d-flex justify-content-between align-items-center">
                  <span class="text-warning">Email đáng ngờ:</span>
                  <b-badge variant="warning" pill>{{ stats.categories.suspicious?.count || 0 }}</b-badge>
                </b-list-group-item>
                <b-list-group-item class="d-flex justify-content-between align-items-center">
                  <span class="text-secondary">Email spam:</span>
                  <b-badge variant="secondary" pill>{{ stats.categories.spam?.count || 0 }}</b-badge>
                </b-list-group-item>
                <b-list-group-item class="d-flex justify-content-between align-items-center">
                  <span class="text-danger">Email lừa đảo:</span>
                  <b-badge variant="danger" pill>{{ stats.categories.phishing?.count || 0 }}</b-badge>
                </b-list-group-item>
              </b-list-group>
            </div>
          </b-col>
        </b-row>
      </b-card>

      <b-card class="mb-4">
        <h3 class="mb-4">Xu hướng theo thời gian</h3>
        <apexchart 
          type="area"
          height="350"
          :options="trendChartOptions"
          :series="trendChartSeries"
        ></apexchart>
      </b-card>

      <b-card>
        <h3 class="mb-4">Các loại lừa đảo phổ biến</h3>
        <b-table
          :items="commonThreats"
          :fields="threatFields"
          striped
          hover
          responsive
        >
          <template #cell(threat_level)="data">
            <b-badge :variant="getThreatVariant(data.value)">{{ data.value }}</b-badge>
          </template>
          <template #cell(percentage)="data">
            <div class="d-flex align-items-center">
              <b-progress 
                :value="data.value" 
                :variant="getPercentVariant(data.value)" 
                height="10px" 
                class="flex-grow-1 mr-2">
              </b-progress>
              <span>{{ data.value }}%</span>
            </div>
          </template>
        </b-table>
      </b-card>
    </b-overlay>
  </div>
</template>

<script>
import { mapState } from 'vuex';
import VueApexCharts from 'vue-apexcharts';

export default {
  name: 'ReportView',
  components: {
    apexchart: VueApexCharts
  },
  data() {
    return {
      startDate: '',
      endDate: '',
      loading: false,
      today: new Date().toISOString().slice(0, 10),
      threatFields: [
        { key: 'description', label: 'Loại lừa đảo' },
        { key: 'threat_level', label: 'Mức độ nguy hiểm' },
        { key: 'percentage', label: 'Tỷ lệ phát hiện' }
      ],
      commonThreats: [
        { description: 'Giả mạo tài khoản ngân hàng', threat_level: 'Nghiêm trọng', percentage: 35 },
        { description: 'Yêu cầu cập nhật thông tin cá nhân', threat_level: 'Cao', percentage: 25 },
        { description: 'Thông báo trúng thưởng giả mạo', threat_level: 'Trung bình', percentage: 15 },
        { description: 'Email hỗ trợ kỹ thuật giả mạo', threat_level: 'Cao', percentage: 18 },
        { description: 'Liên kết đến trang web lừa đảo', threat_level: 'Nghiêm trọng', percentage: 30 }
      ]
    };
  },
  computed: {
    ...mapState(['stats']),
    
    pieChartOptions() {
      return {
        chart: {
          type: 'pie',
          fontFamily: 'Roboto, sans-serif'
        },
        labels: ['An toàn', 'Đáng ngờ', 'Spam', 'Lừa đảo', 'Chưa phân loại'],
        colors: ['#28a745', '#ffc107', '#6c757d', '#dc3545', '#17a2b8'],
        legend: {
          position: 'bottom'
        },
        responsive: [{
          breakpoint: 480,
          options: {
            chart: {
              width: 300
            },
            legend: {
              position: 'bottom'
            }
          }
        }]
      };
    },
    
    pieChartSeries() {
      if (!this.stats || !this.stats.categories) {
        return [0, 0, 0, 0, 0];
      }
      
      return [
        this.stats.categories.safe?.count || 0,
        this.stats.categories.suspicious?.count || 0,
        this.stats.categories.spam?.count || 0,
        this.stats.categories.phishing?.count || 0,
        this.stats.categories.unknown?.count || 0
      ];
    },
    
    trendChartOptions() {
      return {
        chart: {
          type: 'area',
          height: 350,
          zoom: {
            enabled: false
          },
          toolbar: {
            show: false
          }
        },
        dataLabels: {
          enabled: false
        },
        stroke: {
          curve: 'smooth',
          width: 2
        },
        colors: ['#28a745', '#ffc107', '#6c757d', '#dc3545'],
        fill: {
          type: 'gradient',
          gradient: {
            shadeIntensity: 1,
            opacityFrom: 0.7,
            opacityTo: 0.3
          }
        },
        xaxis: {
          categories: this.getDateCategories(),
          labels: {
            rotate: -45,
            style: {
              fontSize: '12px'
            }
          }
        },
        yaxis: {
          title: {
            text: 'Số lượng email'
          }
        },
        legend: {
          position: 'top'
        }
      };
    },
    
    trendChartSeries() {
      return [
        {
          name: 'An toàn',
          data: this.generateRandomData(7, 10, 25)
        },
        {
          name: 'Đáng ngờ',
          data: this.generateRandomData(7, 5, 15)
        },
        {
          name: 'Spam',
          data: this.generateRandomData(7, 8, 20)
        },
        {
          name: 'Lừa đảo',
          data: this.generateRandomData(7, 3, 12)
        }
      ];
    }
  },
  methods: {
    generateReport() {
      this.loading = true;
      
      // Giả định lấy dữ liệu từ API
      setTimeout(() => {
        this.loading = false;
      }, 1500);
    },
    
    getDateCategories() {
      const dates = [];
      const today = new Date();
      
      for (let i = 6; i >= 0; i--) {
        const date = new Date();
        date.setDate(today.getDate() - i);
        dates.push(date.toLocaleDateString('vi-VN', { day: '2-digit', month: '2-digit' }));
      }
      
      return dates;
    },
    
    generateRandomData(count, min, max) {
      return Array.from({ length: count }, () => 
        Math.floor(Math.random() * (max - min + 1)) + min
      );
    },
    
    getThreatVariant(level) {
      switch (level) {
        case 'Nghiêm trọng': return 'danger';
        case 'Cao': return 'warning';
        case 'Trung bình': return 'info';
        default: return 'secondary';
      }
    },
    
    getPercentVariant(value) {
      if (value > 30) return 'danger';
      if (value > 20) return 'warning';
      return 'info';
    }
  },
  created() {
    // Tải dữ liệu thống kê
    this.$store.dispatch('fetchStats');
  }
};
</script>

<style scoped>
.stats-summary {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.card {
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
}

.progress {
  height: 10px;
  border-radius: 5px;
}
</style> 