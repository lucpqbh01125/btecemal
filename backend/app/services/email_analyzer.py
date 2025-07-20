import re
import json
from urllib.parse import urlparse
from typing import Dict, List, Any, Tuple, Optional

class EmailAnalyzer:
    """
    Service phân tích email để phát hiện phishing, spam, và các email đáng ngờ
    """
    def __init__(self):
        self.load_rules()
        
    def load_rules(self):
        """Tải các quy tắc phân tích email"""
        
        # Các domain phishing phổ biến
        self.phishing_domains = [
            'secure-banking.com', 'account-verify.net', 'login-secure-portal.com',
            'my-account-verify.com', 'secure-login-info.com', 'verification-account.com',
            'paypal-secure.com', 'facebook-security.com', 'apple-id-secure.com',
            'bank-secure-login.com', 'verify-account-now.com', 'secure-verify.xyz'
        ]
        
        # Các domain hợp pháp
        self.legitimate_domains = [
            'google.com', 'facebook.com', 'microsoft.com', 'apple.com',
            'amazon.com', 'paypal.com', 'netflix.com', 'gmail.com',
            'outlook.com', 'yahoo.com', 'spotify.com', 'linkedin.com'
        ]
        
        # Từ khóa spam tiếng Việt và tiếng Anh
        self.spam_words = [
            'free', 'miễn phí', 'urgent', 'khẩn cấp', 'lottery', 'xổ số', 'winner', 'trúng thưởng',
            'million dollar', 'triệu đô', 'limited time', 'viagra', 'enlarge', 'cheap', 'rẻ', 
            'discount', 'giảm giá', 'cash', 'tiền mặt', 'offer', 'ưu đãi', 'exclusive', 'độc quyền',
            'congratulation', 'chúc mừng', 'prize', 'giải thưởng', 'win', 'chiến thắng',
            'free money', 'tiền miễn phí', 'best offer', 'ưu đãi tốt nhất', 'best price', 'giá tốt nhất',
            'act now', 'hành động ngay', 'limited offer', 'ưu đãi có hạn', 'only today', 'chỉ hôm nay',
            'call now', 'gọi ngay', 'click here', 'nhấp vào đây', 'click below', 'nhấp vào bên dưới',
            'unbelievable', 'không thể tin được', 'incredible', 'không thể tin', 'amazing', 'tuyệt vời',
            'guarantee', 'đảm bảo', '100% free', '100% miễn phí', 'no cost', 'không tốn phí'
        ]
        
        # Các cụm từ phishing phổ biến tiếng Việt và tiếng Anh
        self.phishing_phrases = [
            'verify your account', 'xác minh tài khoản', 
            'confirm your password', 'xác nhận mật khẩu',
            'update your payment', 'cập nhật thanh toán', 
            'unusual activity', 'hoạt động bất thường',
            'suspicious login', 'đăng nhập đáng ngờ', 
            'account suspended', 'tài khoản bị đình chỉ',
            'click here to verify', 'nhấp vào đây để xác minh',
            'login to update', 'đăng nhập để cập nhật',
            'confirm your identity', 'xác nhận danh tính của bạn',
            'security alert', 'cảnh báo bảo mật',
            'account will be terminated', 'tài khoản sẽ bị chấm dứt',
            'verify now or lose access', 'xác minh ngay hoặc mất quyền truy cập',
            'unauthorized purchase', 'giao dịch không được ủy quyền',
            'verify billing information', 'xác minh thông tin thanh toán',
            'update required', 'yêu cầu cập nhật',
            'account verification required', 'yêu cầu xác minh tài khoản',
            'your account has been limited', 'tài khoản của bạn đã bị giới hạn',
            'payment declined', 'thanh toán bị từ chối',
            'problem with your account', 'vấn đề với tài khoản của bạn',
            'click to recover account', 'nhấp để khôi phục tài khoản'
        ]
        
        # Từ khóa khẩn cấp
        self.urgency_words = [
            'urgent', 'khẩn cấp', 'immediately', 'ngay lập tức', 
            'now', 'right now', 'ngay bây giờ', 'expiring', 'sắp hết hạn',
            'today only', 'chỉ hôm nay', 'limited time', 'thời gian có hạn',
            'deadline', 'hạn cuối', 'act fast', 'hành động nhanh',
            'final notice', 'thông báo cuối cùng', 'last chance', 'cơ hội cuối',
            'expires today', 'hết hạn hôm nay', 'don\'t delay', 'đừng trì hoãn',
            'urgent action required', 'yêu cầu hành động khẩn cấp',
            'time sensitive', 'nhạy cảm về thời gian',
            'respond now', 'phản hồi ngay', 'immediate action', 'hành động ngay lập tức'
        ]
        
        # TLDs đáng ngờ
        self.suspicious_tlds = ['.xyz', '.tk', '.ml', '.ga', '.cf', '.gq', '.top', '.icu', '.work', '.info']

    def analyze_email(self, title: str, content: str, sender: str = '') -> Dict[str, Any]:
        """
        Phân tích email dựa trên nội dung, tiêu đề và người gửi
        
        Args:
            title: Tiêu đề email
            content: Nội dung email
            sender: Email người gửi
            
        Returns:
            Dict chứa kết quả phân tích
        """
        
        # Trích xuất các đặc trưng
        url_count = len(re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', content))
        has_urgency = any(word in (title + content).lower() for word in self.urgency_words)
        has_suspicious_sender = self._check_suspicious_sender(sender)
        
        # Kiểm tra các dấu hiệu phishing phổ biến
        contains_phishing_phrases = any(phrase in (title + content).lower() for phrase in self.phishing_phrases)
        spam_word_count = sum(1 for word in self.spam_words if word in (title + content).lower())
        
        # Kiểm tra URL đáng ngờ
        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', content)
        suspicious_urls = sum(1 for url in urls if self._is_suspicious_url(url))
        
        # Sử dụng rule-based để tính điểm và phân loại
        score = 0
        
        # Tính điểm dựa trên các chỉ số
        if has_suspicious_sender:
            score += 25
        
        if contains_phishing_phrases:
            score += 30
        
        score += spam_word_count * 5  # 5 điểm cho mỗi từ khóa spam
        score += suspicious_urls * 30  # Tăng từ 20 lên 30 điểm cho mỗi URL đáng ngờ
        
        if has_urgency:
            score += 15
        
        # Giới hạn điểm tối đa là 100
        confidence_score = min(score, 100)
        
        # Xác định danh mục dựa trên điểm và các yếu tố khác
        if contains_phishing_phrases and (suspicious_urls > 0 or has_suspicious_sender):
            # Nếu có cụm từ lừa đảo VÀ có URL đáng ngờ hoặc người gửi đáng ngờ => Là lừa đảo
            category = 'phishing'
            category_id = 5
            confidence_score = max(confidence_score, 80)  # Đảm bảo điểm đủ cao cho lừa đảo
        elif confidence_score < 30:
            category = 'safe'
            category_id = 2
        elif confidence_score < 55:
            category = 'suspicious'
            category_id = 3
        elif confidence_score < 75:
            category = 'spam'
            category_id = 4
        else:
            category = 'phishing'
            category_id = 5
            
        # Xác định mức độ
        if confidence_score < 30:
            level = 'low'
        elif confidence_score < 55:
            level = 'medium'
        elif confidence_score < 75:
            level = 'high'
        else:
            level = 'critical'
            
        # Tạo các lý do
        reasons = []
        if contains_phishing_phrases:
            reasons.append("Phát hiện cụm từ lừa đảo trong nội dung")
        if has_suspicious_sender:
            reasons.append("Người gửi email có dấu hiệu đáng ngờ")
        if spam_word_count > 3:
            reasons.append(f"Phát hiện {spam_word_count} từ khóa spam")
        if suspicious_urls > 0:
            reasons.append(f"Phát hiện {suspicious_urls} URL đáng ngờ")
        if has_urgency:
            reasons.append("Email sử dụng từ ngữ tạo cảm giác khẩn cấp")
        
        # Tổng hợp các chỉ số đáng ngờ
        suspicious_indicators = {
            'urls_count': url_count,
            'suspicious_urls': suspicious_urls if urls else 0,
            'urgency_indicators': has_urgency,
            'suspicious_sender': has_suspicious_sender,
            'spam_word_count': spam_word_count,
            'contains_phishing_phrases': contains_phishing_phrases,
            'reasons': reasons
        }
        
        return {
            'category': category,
            'category_id': category_id,
            'confidence_score': confidence_score,
            'level': level,
            'suspicious_indicators': suspicious_indicators,
            'recommendation': self._get_recommendation(category)
        }
    
    def verify_sender(self, sender: str) -> Dict[str, Any]:
        """
        Xác minh người gửi email có đáng tin hay không
        
        Args:
            sender: Email người gửi
            
        Returns:
            Dict chứa kết quả xác minh
        """
        if not sender or '@' not in sender:
            return {'valid': False, 'reason': 'Định dạng email không hợp lệ', 'confidence_score': 50}
        
        domain = sender.split('@')[-1]
        
        # Kiểm tra với các domain phishing đã biết
        if any(phish_domain in domain for phish_domain in self.phishing_domains):
            return {
                'valid': False,
                'reason': 'Domain liên quan đến phishing',
                'confidence_score': 90
            }
        
        # Kiểm tra với các domain hợp pháp đã biết
        if any(legit_domain in domain for legit_domain in self.legitimate_domains):
            return {
                'valid': True,
                'reason': 'Domain có vẻ hợp pháp',
                'confidence_score': 10
            }
        
        # Kiểm tra TLDs đáng ngờ
        if any(domain.endswith(tld) for tld in self.suspicious_tlds):
            return {
                'valid': False,
                'reason': 'Tên miền cấp cao nhất (TLD) đáng ngờ',
                'confidence_score': 70
            }
        
        return {
            'valid': True,
            'reason': 'Domain có vẻ bình thường nhưng cần xác minh nếu không quen thuộc',
            'confidence_score': 40
        }
    
    def check_link(self, url: str) -> Dict[str, Any]:
        """
        Kiểm tra URL có khả năng độc hại hay không
        
        Args:
            url: URL cần kiểm tra
            
        Returns:
            Dict chứa kết quả kiểm tra
        """
        if not url:
            return {'safe': False, 'reason': 'URL trống', 'confidence_score': 50}
        
        try:
            parsed = urlparse(url)
            domain = parsed.netloc
            
            # Kiểm tra TLDs đáng ngờ
            if any(domain.endswith(tld) for tld in self.suspicious_tlds):
                return {
                    'safe': False,
                    'reason': 'Tên miền cấp cao nhất đáng ngờ',
                    'confidence_score': 80
                }
            
            # Kiểm tra URL sử dụng địa chỉ IP
            if re.match(r'^(\d{1,3}\.){3}\d{1,3}$', domain):
                return {
                    'safe': False,
                    'reason': 'URL sử dụng địa chỉ IP thay vì tên miền',
                    'confidence_score': 85
                }
            
            # Kiểm tra URL rút gọn
            shorteners = ['bit.ly', 'tinyurl.com', 'goo.gl', 't.co', 'is.gd', 'buff.ly', 'ow.ly', 'rebrand.ly', 'cutt.ly']
            if any(shortener in domain for shortener in shorteners):
                return {
                    'safe': False,
                    'reason': 'Sử dụng URL rút gọn có thể che giấu điểm đến thực sự',
                    'confidence_score': 60
                }
            
            # Kiểm tra các misspelling của các tên miền phổ biến
            popular_domains = ['google', 'facebook', 'microsoft', 'apple', 'amazon', 'paypal', 'netflix']
            for pop_domain in popular_domains:
                if pop_domain in domain and pop_domain + '.com' != domain:
                    return {
                        'safe': False,
                        'reason': f'Có thể là giả mạo của {pop_domain}.com',
                        'confidence_score': 90
                    }
            
            # Kiểm tra với các domain phishing đã biết
            if any(phish_domain in domain for phish_domain in self.phishing_domains):
                return {
                    'safe': False,
                    'reason': 'Domain được biết đến là độc hại',
                    'confidence_score': 95
                }
            
            # Kiểm tra các domain hợp pháp
            if any(legit_domain in domain for legit_domain in self.legitimate_domains):
                return {
                    'safe': True,
                    'reason': 'Domain có vẻ an toàn',
                    'confidence_score': 15
                }
                
            return {
                'safe': True,
                'reason': 'URL không có dấu hiệu đáng ngờ rõ ràng nhưng cần thận trọng',
                'confidence_score': 40
            }
            
        except Exception as e:
            return {
                'safe': False,
                'reason': f'Lỗi khi phân tích URL: {str(e)}',
                'confidence_score': 60
            }
    
    def _check_suspicious_sender(self, sender: str) -> bool:
        """
        Kiểm tra người gửi email có đáng ngờ không
        
        Args:
            sender: Email người gửi
            
        Returns:
            True nếu người gửi đáng ngờ, ngược lại là False
        """
        if not sender or '@' not in sender:
            return True
            
        domain = sender.split('@')[-1].lower()
        
        # Kiểm tra TLDs đáng ngờ
        if any(domain.endswith(tld) for tld in self.suspicious_tlds):
            return True
            
        # Kiểm tra domain phishing
        if any(phish_domain in domain for phish_domain in self.phishing_domains):
            return True
            
        # Kiểm tra các misspelling và giả mạo của tên miền phổ biến
        popular_domains = [
            'google.com', 'gmail.com', 'outlook.com', 'yahoo.com', 
            'microsoft.com', 'facebook.com', 'apple.com', 'amazon.com',
            'paypal.com', 'netflix.com'
        ]
        
        # Phát hiện các giả mạo như g00gle thay vì google, m1crosoft thay vì microsoft
        for pop_domain in popular_domains:
            base_name = pop_domain.split('.')[0]
            # Nếu domain chứa tên miền phổ biến nhưng không chính xác là tên miền đó
            if base_name in domain.lower() and pop_domain != domain:
                # Kiểm tra thêm các thay thế số cho chữ (0 thay o, 1 thay i/l...)
                if (base_name.replace('o', '0') in domain or
                    base_name.replace('i', '1') in domain or
                    base_name.replace('l', '1') in domain or
                    base_name.replace('e', '3') in domain or
                    base_name.replace('a', '4') in domain or
                    base_name.replace('s', '5') in domain):
                    return True
                    
                # Kiểm tra thêm các thêm gạch ngang hoặc ký tự đặc biệt
                if f"-{base_name}" in domain or f"{base_name}-" in domain:
                    return True
                    
                # Phát hiện misspelling nhẹ (thêm, bớt, hoặc thay thế 1-2 ký tự)
                if len(set(base_name) - set(domain)) <= 2:
                    return True
                
        return False
    
    def _is_suspicious_url(self, url: str) -> bool:
        """
        Kiểm tra URL có đáng ngờ không
        
        Args:
            url: URL cần kiểm tra
            
        Returns:
            True nếu URL đáng ngờ, ngược lại là False
        """
        try:
            parsed = urlparse(url)
            domain = parsed.netloc
            
            # Kiểm tra URL sử dụng địa chỉ IP
            if re.match(r'^(\d{1,3}\.){3}\d{1,3}$', domain):
                return True
                
            # Kiểm tra TLDs đáng ngờ
            if any(domain.endswith(tld) for tld in self.suspicious_tlds):
                return True
            
            # Kiểm tra domain có chứa .xyz
            if '.xyz' in domain:
                return True
                
            # Kiểm tra URL rút gọn
            shorteners = ['bit.ly', 'tinyurl.com', 'goo.gl', 't.co', 'is.gd', 'buff.ly', 'ow.ly']
            if any(shortener in domain for shortener in shorteners):
                return True
                
            # Kiểm tra domain phishing
            if any(phish_domain in domain for phish_domain in self.phishing_domains):
                return True
                
            # Kiểm tra các misspelling của tên miền phổ biến
            popular_domains = ['google', 'facebook', 'microsoft', 'apple', 'amazon', 'paypal']
            for pop_domain in popular_domains:
                if pop_domain in domain and pop_domain + '.com' != domain:
                    return True
            
            # Kiểm tra domain có chứa 'secure', 'verify' hoặc 'account' cùng với đuôi không phổ biến
            suspicious_words = ['secure', 'verify', 'account', 'login', 'banking']
            if any(word in domain.lower() for word in suspicious_words) and not any(domain.endswith('.' + legit) for legit in ['com', 'org', 'net', 'edu', 'gov']):
                return True
                    
            return False
            
        except Exception:
            return True  # Nếu không thể phân tích URL, coi là đáng ngờ
    
    def _get_recommendation(self, category: str) -> str:
        """
        Tạo khuyến nghị dựa trên loại email
        
        Args:
            category: Loại email (phishing, spam, suspicious, safe)
            
        Returns:
            Chuỗi chứa khuyến nghị
        """
        if category == "phishing":
            return "Email này có dấu hiệu lừa đảo. Không nhấp vào liên kết hoặc cung cấp thông tin cá nhân."
        elif category == "suspicious":
            return "Email này có một số dấu hiệu đáng ngờ. Xác minh thông tin trước khi thực hiện bất kỳ hành động nào."
        elif category == "spam":
            return "Đây là thư rác quảng cáo. Nên bỏ qua hoặc chặn người gửi."
        else:
            return "Email này có vẻ an toàn, nhưng vẫn nên cẩn thận khi mở các tệp đính kèm hoặc nhấp vào liên kết." 