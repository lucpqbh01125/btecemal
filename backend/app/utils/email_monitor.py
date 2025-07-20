import imaplib
import email
from email.header import decode_header
import datetime
from typing import List, Dict, Any, Optional
import logging

# Cấu hình logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EmailMonitor:
    """
    Lớp để theo dõi và lấy email từ server IMAP
    """
    def __init__(self, 
                 email_address: str, 
                 password: str, 
                 imap_server: str = "imap.gmail.com",
                 imap_port: int = 993):
        self.email_address = email_address
        self.password = password
        self.imap_server = imap_server
        self.imap_port = imap_port
        self._imap = None

    def connect(self) -> bool:
        """
        Kết nối tới server IMAP
        """
        try:
            self._imap = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            self._imap.login(self.email_address, self.password)
            return True
        except Exception as e:
            logger.error(f"Lỗi kết nối IMAP: {str(e)}")
            return False

    def disconnect(self):
        """
        Ngắt kết nối khỏi server IMAP
        """
        if self._imap:
            try:
                self._imap.logout()
            except:
                pass
            self._imap = None

    def get_emails(self, folder: str = "INBOX", limit: int = 10, 
                   since_date: Optional[datetime.date] = None) -> List[Dict[str, Any]]:
        """
        Lấy danh sách email từ một thư mục cụ thể
        """
        if not self._imap:
            if not self.connect():
                return []

        emails_data = []
        try:
            # Chọn thư mục
            status, messages = self._imap.select(folder)
            
            # Tạo điều kiện tìm kiếm
            search_criteria = "ALL"
            if since_date:
                date_str = since_date.strftime("%d-%b-%Y")
                search_criteria = f'(SINCE "{date_str}")'
            
            # Tìm kiếm email
            status, messages = self._imap.search(None, search_criteria)
            if status != "OK":
                logger.warning(f"Không thể tìm kiếm email: {status}")
                return []
            
            # Lấy danh sách ID
            email_ids = messages[0].split()
            
            # Giới hạn số lượng email
            if limit > 0:
                email_ids = email_ids[-limit:]
            
            # Lấy thông tin từng email
            for e_id in reversed(email_ids):
                status, msg_data = self._imap.fetch(e_id, "(RFC822)")
                if status != "OK":
                    continue
                
                # Parse email
                msg = email.message_from_bytes(msg_data[0][1])
                
                # Lấy thông tin email
                subject = self._decode_header(msg["Subject"])
                from_addr = self._decode_header(msg["From"])
                to_addr = self._decode_header(msg["To"])
                date = self._decode_header(msg["Date"])
                
                # Lấy nội dung
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        
                        # Chỉ lấy phần text
                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            try:
                                body = part.get_payload(decode=True).decode()
                            except:
                                pass
                else:
                    try:
                        body = msg.get_payload(decode=True).decode()
                    except:
                        body = msg.get_payload()
                
                # Thêm vào danh sách kết quả
                email_data = {
                    "id": e_id.decode(),
                    "subject": subject,
                    "from": from_addr,
                    "to": to_addr,
                    "date": date,
                    "body": body
                }
                emails_data.append(email_data)
            
            return emails_data
            
        except Exception as e:
            logger.error(f"Lỗi khi lấy email: {str(e)}")
            return []

    def _decode_header(self, header):
        """
        Decode email header
        """
        if header is None:
            return ""
            
        try:
            decoded_headers = decode_header(header)
            header_parts = []
            
            for decoded_text, charset in decoded_headers:
                if isinstance(decoded_text, bytes):
                    if charset:
                        try:
                            decoded_text = decoded_text.decode(charset)
                        except:
                            decoded_text = decoded_text.decode('utf-8', errors='replace')
                    else:
                        decoded_text = decoded_text.decode('utf-8', errors='replace')
                header_parts.append(str(decoded_text))
                
            return " ".join(header_parts)
        except:
            return str(header)

if __name__ == "__main__":
    # Ví dụ sử dụng
    monitor = EmailMonitor(
        email_address="your_email@gmail.com",
        password="your_password"
    )
    
    if monitor.connect():
        print("Kết nối thành công!")
        emails = monitor.get_emails(limit=5)
        for email in emails:
            print(f"Subject: {email['subject']}")
            print(f"From: {email['from']}")
            print("-" * 50)
        
        monitor.disconnect()
    else:
        print("Không thể kết nối đến server IMAP") 