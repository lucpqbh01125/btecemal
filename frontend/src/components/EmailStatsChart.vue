<template>
  <div>
    <b-tabs content-class="mt-3">
      <b-tab title="Phân loại" active>
        <div class="chart-container">
          <apexchart
            type="pie"
            height="320"
            :options="pieChartOptions"
            :series="pieChartSeries"
          ></apexchart>
        </div>
      </b-tab>
      <b-tab title="Xu hướng">
        <div v-if="stats.recent_trend && stats.recent_trend.length > 0" class="chart-container">
          <apexchart
            type="area"
            height="320"
            :options="trendChartOptions"
            :series="trendChartSeries"
          ></apexchart>
        </div>
        <div v-else class="text-center p-5">
          <b-icon-graph-down font-scale="3"></b-icon-graph-down>
          <p class="mt-3">Không đủ dữ liệu để hiển thị xu hướng</p>
        </div>
      </b-tab>
    </b-tabs>
  </div>
</template>

<script>
import { mapState } from 'vuex';
import VueApexCharts from 'vue-apexcharts';
import { BIconGraphDown } from 'bootstrap-vue';

export default {
  name: 'EmailStatsChart',
  components: {
    apexchart: VueApexCharts,
    BIconGraphDown
  },
  computed: {
    ...mapState(['stats', 'loading']),
    
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
    
    pieChartOptions() {
      return {
        chart: {
          type: 'pie',
          fontFamily: 'Roboto, sans-serif',
          toolbar: {
            show: false
          }
        },
        labels: ['An toàn', 'Đáng ngờ', 'Spam', 'Lừa đảo', 'Chưa phân loại'],
        colors: ['#28a745', '#ffc107', '#6c757d', '#dc3545', '#17a2b8'],
        legend: {
          position: 'bottom',
          horizontalAlign: 'center'
        },
        plotOptions: {
          pie: {
            dataLabels: {
              offset: -10
            }
          }
        },
        dataLabels: {
          formatter(val, opts) {
            const name = opts.w.globals.labels[opts.seriesIndex];
            const count = opts.w.globals.seriesTotals[opts.seriesIndex];
            return [name, `${count} (${val.toFixed(1)}%)`];
          }
        },
        tooltip: {
          y: {
            formatter: (value) => {
              return `${value} email`;
            }
          }
        },
        responsive: [
          {
            breakpoint: 480,
            options: {
              chart: {
                height: 300
              },
              legend: {
                position: 'bottom'
              }
            }
          }
        ]
      };
    },
    
    trendChartSeries() {
      if (!this.stats || !this.stats.recent_trend || this.stats.recent_trend.length === 0) {
        return [];
      }
      
      return [
        {
          name: 'An toàn',
          data: this.stats.recent_trend.map(day => day.safe || 0)
        },
        {
          name: 'Đáng ngờ',
          data: this.stats.recent_trend.map(day => day.suspicious || 0)
        },
        {
          name: 'Spam',
          data: this.stats.recent_trend.map(day => day.spam || 0)
        },
        {
          name: 'Lừa đảo',
          data: this.stats.recent_trend.map(day => day.phishing || 0)
        },
        {
          name: 'Chưa phân loại',
          data: this.stats.recent_trend.map(day => day.unknown || 0)
        }
      ];
    },
    
    trendChartOptions() {
      return {
        chart: {
          type: 'area',
          height: 320,
          fontFamily: 'Roboto, sans-serif',
          toolbar: {
            show: false
          },
          zoom: {
            enabled: false
          }
        },
        colors: ['#28a745', '#ffc107', '#6c757d', '#dc3545', '#17a2b8'],
        dataLabels: {
          enabled: false
        },
        stroke: {
          curve: 'smooth',
          width: 2
        },
        fill: {
          type: 'gradient',
          gradient: {
            shadeIntensity: 1,
            opacityFrom: 0.7,
            opacityTo: 0.3,
            stops: [0, 90, 100]
          }
        },
        xaxis: {
          categories: this.stats.recent_trend ? this.stats.recent_trend.map(day => this.formatDate(day.date)) : [],
          tooltip: {
            enabled: false
          }
        },
        yaxis: {
          labels: {
            formatter: (value) => {
              return Math.floor(value);
            }
          }
        },
        legend: {
          position: 'top',
          horizontalAlign: 'center',
          offsetY: 0
        },
        tooltip: {
          shared: true,
          y: {
            formatter: (value) => {
              return `${value} email`;
            }
          }
        }
      };
    }
  },
  methods: {
    formatDate(dateStr) {
      if (!dateStr) return '';
      const options = { day: '2-digit', month: '2-digit' };
      return new Date(dateStr).toLocaleDateString('vi-VN', options);
    }
  }
};
</script>

<style scoped>
.chart-container {
  min-height: 320px;
  position: relative;
}
</style> 