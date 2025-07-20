<template>
  <div id="app">
    <b-navbar toggleable="lg" type="dark" variant="primary" fixed="top">
      <b-navbar-brand to="/">
        <b-icon-shield-check class="mr-1"></b-icon-shield-check>
        Email Analyzer
      </b-navbar-brand>

      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item to="/" exact>Dashboard</b-nav-item>
          <b-nav-item to="/check-email">Kiểm tra Email</b-nav-item>
          <b-nav-item to="/education">Hướng dẫn phòng tránh</b-nav-item>
          <b-nav-item to="/report">Báo cáo phân tích</b-nav-item>
        </b-navbar-nav>

        <b-navbar-nav class="ml-auto">
          <b-nav-item-dropdown right>
            <template #button-content>
              <b-icon-gear></b-icon-gear> Cài đặt
            </template>
            <b-dropdown-item href="#">Tùy chọn</b-dropdown-item>
            <b-dropdown-item href="#">Cấu hình</b-dropdown-item>
            <b-dropdown-divider></b-dropdown-divider>
            <b-dropdown-item href="#"><b-icon-power></b-icon-power> Đăng xuất</b-dropdown-item>
          </b-nav-item-dropdown>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>

    <div class="content-container">
      <router-view/>
    </div>

    <b-navbar type="dark" variant="secondary" fixed="bottom" class="footer">
      <b-navbar-nav class="ml-auto">
        <b-nav-text>&copy; {{ currentYear }} Email Analyzer System</b-nav-text>
      </b-navbar-nav>
    </b-navbar>
  </div>
</template>

<script>
import { BIconShieldCheck, BIconGear, BIconPower } from 'bootstrap-vue';

export default {
  name: 'App',
  components: {
    BIconShieldCheck,
    BIconGear,
    BIconPower
  },
  computed: {
    currentYear() {
      return new Date().getFullYear();
    }
  }
}
</script>

<style>
#app {
  font-family: 'Roboto', 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

.content-container {
  margin-top: 60px;
  margin-bottom: 40px;
  padding: 20px;
}

.footer {
  height: 40px;
  padding: 0 20px;
}

/* Override Bootstrap styles */
.nav-link.router-link-exact-active {
  font-weight: bold;
  color: #fff !important;
}
</style> 