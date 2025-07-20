<template>
  <div>
    <h1 class="mb-4">Hướng dẫn phòng tránh email lừa đảo</h1>

    <b-card class="mb-4">
      <h3>1. Những dấu hiệu nhận biết email lừa đảo</h3>
      <b-list-group class="mb-3">
        <b-list-group-item>
          <strong>Địa chỉ người gửi đáng ngờ:</strong> 
          Email lừa đảo thường đến từ địa chỉ giả mạo các công ty, tổ chức lớn nhưng có sự khác biệt nhỏ (ví dụ: support@paypa1.com thay vì support@paypal.com).
        </b-list-group-item>
        <b-list-group-item>
          <strong>Lỗi chính tả và ngữ pháp:</strong> 
          Email lừa đảo thường chứa nhiều lỗi chính tả, ngữ pháp hoặc câu cú bất thường.
        </b-list-group-item>
        <b-list-group-item>
          <strong>Tạo cảm giác khẩn cấp:</strong>
          Email lừa đảo thường yêu cầu hành động ngay lập tức để tạo áp lực, như "tài khoản của bạn sẽ bị khóa trong 24 giờ".
        </b-list-group-item>
        <b-list-group-item>
          <strong>Yêu cầu thông tin cá nhân:</strong>
          Các tổ chức hợp pháp thường không yêu cầu thông tin nhạy cảm qua email như mật khẩu, thông tin thẻ tín dụng.
        </b-list-group-item>
        <b-list-group-item>
          <strong>Đường link và tệp đính kèm đáng ngờ:</strong>
          Cẩn thận với các đường link lạ hoặc các tệp đính kèm không mong đợi, đặc biệt là các file .exe, .zip, hoặc .docm.
        </b-list-group-item>
      </b-list-group>
    </b-card>

    <b-card class="mb-4">
      <h3>2. Các biện pháp phòng tránh</h3>
      <b-list-group class="mb-3">
        <b-list-group-item>
          <strong>Kiểm tra địa chỉ người gửi:</strong> 
          Luôn xem xét kỹ địa chỉ email của người gửi, không chỉ tên hiển thị.
        </b-list-group-item>
        <b-list-group-item>
          <strong>Không nhấp vào đường link đáng ngờ:</strong> 
          Di chuột qua (hover) để xem URL thực sự trước khi nhấp vào. Tốt nhất là truy cập trực tiếp vào trang web chính thức thay vì qua link trong email.
        </b-list-group-item>
        <b-list-group-item>
          <strong>Không tải các tệp đính kèm đáng ngờ:</strong>
          Nếu bạn không chắc chắn về nguồn gốc của email, đừng mở các tệp đính kèm.
        </b-list-group-item>
        <b-list-group-item>
          <strong>Sử dụng xác thực hai yếu tố:</strong>
          Bật xác thực hai yếu tố cho tất cả tài khoản quan trọng để tăng thêm lớp bảo vệ.
        </b-list-group-item>
        <b-list-group-item>
          <strong>Cập nhật phần mềm thường xuyên:</strong>
          Luôn cập nhật hệ điều hành, trình duyệt, và phần mềm bảo mật để có được các bản vá bảo mật mới nhất.
        </b-list-group-item>
      </b-list-group>
    </b-card>

    <b-card class="mb-4">
      <h3>3. Khi nghi ngờ bị lừa đảo</h3>
      <b-list-group class="mb-3">
        <b-list-group-item>
          <strong>Không cung cấp thông tin:</strong>
          Dừng mọi tương tác và không cung cấp bất kỳ thông tin nào.
        </b-list-group-item>
        <b-list-group-item>
          <strong>Thay đổi mật khẩu:</strong>
          Nếu bạn đã nhấp vào liên kết hoặc nhập thông tin, hãy thay đổi mật khẩu của tài khoản liên quan ngay lập tức.
        </b-list-group-item>
        <b-list-group-item>
          <strong>Báo cáo vấn đề:</strong>
          Báo cáo email lừa đảo cho công ty bị giả mạo và các cơ quan có thẩm quyền.
        </b-list-group-item>
        <b-list-group-item>
          <strong>Kiểm tra thiết bị:</strong>
          Quét thiết bị bằng phần mềm diệt virus đáng tin cậy để phát hiện phần mềm độc hại.
        </b-list-group-item>
      </b-list-group>
    </b-card>

    <b-card>
      <h3>4. Sử dụng công cụ phân tích email</h3>
      <p>
        Hệ thống Email Analyzer của chúng tôi giúp bạn phân tích và phát hiện email lừa đảo một cách nhanh chóng và chính xác.
        Chỉ cần sao chép thông tin email vào 
        <b-link to="/check-email" class="font-weight-bold">công cụ kiểm tra</b-link>, 
        hệ thống sẽ đánh giá mức độ nguy hiểm và đưa ra khuyến nghị phù hợp.
      </p>

      <div class="text-center mt-4">
        <b-button to="/check-email" variant="primary" size="lg">
          <b-icon-shield-check class="mr-2"></b-icon-shield-check> Kiểm tra email ngay
        </b-button>
      </div>
    </b-card>
  </div>
</template>

<script>
import { BIconShieldCheck } from 'bootstrap-vue';

export default {
  name: 'EducationView',
  components: {
    BIconShieldCheck
  }
};
</script>

<style scoped>
.card {
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
  margin-bottom: 2rem;
}

.list-group-item {
  border-left: none;
  border-right: none;
}

.list-group-item:first-child {
  border-top: none;
}

.list-group-item:last-child {
  border-bottom: none;
}
</style> 