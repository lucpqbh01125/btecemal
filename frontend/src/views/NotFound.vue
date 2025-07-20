<template>
  <div class="not-found">
    <div class="text-center">
      <h1 class="display-1 mb-4">404</h1>
      <h2 class="mb-4">Trang không tồn tại</h2>
      <p class="lead mb-5">
        Rất tiếc, trang bạn đang tìm kiếm không tồn tại hoặc đã được di chuyển.
      </p>
      <b-button to="/" variant="primary" size="lg">
        <b-icon-house-fill class="mr-2"></b-icon-house-fill>
        Quay về trang chủ
      </b-button>
    </div>
  </div>
</template>

<script>
import { BIconHouseFill } from 'bootstrap-vue';

export default {
  name: 'NotFound',
  components: {
    BIconHouseFill
  }
};
</script>

<style scoped>
.not-found {
  padding: 5rem 0;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
}

.display-1 {
  font-size: 6rem;
  font-weight: 300;
  color: #6c757d;
}
</style> 