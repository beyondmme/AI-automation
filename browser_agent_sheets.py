import os
import asyncio
from datetime import datetime
import json
import gspread
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials

# Các thư viện trong Stack của bạn
from browser_use import Agent
from langchain_community.chat_models import ChatLiteLLM

load_dotenv()

# =====================================================================
# 1. CẤU HÌNH GOOGLE SHEETS (Thay ID của bạn vào dòng 23 nhé)
# =====================================================================
print("1. Đang kết nối tới hệ thống Google Sheets...")
scopes = ["1r_5sg4wKYGJw3ESFOE7vRRfkYGV2wJdGnA2ONQUOAyk"]
creds = Credentials.from_service_account_file("google_creds.json", scopes=scopes)
client = gspread.authorize(creds)

# THAY CHÍNH XÁC ID GOOGLE SHEET CỦA BẠN VÀO GIỮA HAI DẤU NHÁY ĐƠN:
SPREADSHEET_ID = 'ĐIỀN_ID_GOOGLE_SHEET_CỦA_BẠN_VÀO_ĐÂY' 
sheet = client.open_by_key(SPREADSHEET_ID).sheet1


# =====================================================================
# 2. KHỞI TẠO NÃO BỘ AI QUA LITELLM (Sử dụng model Llama 3.3 từ Groq)
# =====================================================================
llm = ChatLiteLLM(model="groq/llama-3.3-70b-versatile", temperature=0.3)


# =====================================================================
# 3. KỊCH BẢN ĐIỀU KHIỂN AGENT SĂN TIN TỨC FEMALE K-POP TOÀN DIỆN
# =====================================================================
async def main():
    # Câu lệnh Prompt chi tiết ép AI quét diện rộng và lọc sâu nhóm nữ ( BLACKPINK, NewJeans, BabyMonster, aespa, IVE,...)
    task_prompt = (
        "1. Open 'https://www.soompi.com/category/music' and scan the latest K-pop news articles. "
        "2. Focus primarily on articles related to female K-pop groups, female idols, or general industry trends that impact female artists. "
        "3. Cover all relevant categories such as: Comeback/Debut announcements, Music Video views/records, Digital Chart achievements (Billboard, Circle, Melon), Brand endorsements, Concept/Creative direction updates, or Agency strategies. "
        "4. Extract the top 5 most critical or trending news items. For each item, capture: "
        "   - The Article Title. "
        "   - The Specific Category (e.g., Comeback, Music Record, Fashion/Branding, Agency Strategy, Concept). "
        "   - A concise summary identifying the key female artists involved (e.g., NewJeans, BLACKPINK, BabyMonster, aespa, IVE, etc.) and what happened. "
        "   - The direct URL link. "
        "5. Output the final result strictly as a raw JSON list of lists (WITHOUT using markdown code blocks like 
http://googleusercontent.com/immersive_entry_chip/0

---

### Cách triển khai "ăn ngay":

1. **Chuẩn bị bảng tính:** Bạn hãy tạo sẵn các tiêu đề cột ở dòng số 1 trong file Google Sheets của bạn để nhìn dữ liệu đổ về trực quan hơn:
   * Cột A: **Thời gian quét**
   * Cột B: **Tiêu đề bài viết**
   * Cột C: **Phân loại (Category)**
   * Cột D: **Tóm tắt & Nghệ sĩ (Summary/Artist)**
   * Cột E: **Đường Link (URL)**
2. **Cập nhật code:** Thay toàn bộ code này vào file `browser_agent_sheets.py` hiện tại, điền ID Sheet của bạn vào dòng 23.
3. **Commit và Chạy:** Đẩy code lên GitHub và bấm nút **Run workflow** quen thuộc ở tab **Actions**. 

Lần này, AI sẽ không lấy tin ngẫu nhiên nữa mà sẽ chủ động đóng vai trò như một **Trợ lý Sáng tạo & Chiến lược chuyên sâu**, lọc ra 5 tin hot nhất về các nhóm nữ K-pop, phân loại rõ ràng từng category và điền gọn gàng vào bảng tính của bạn!
