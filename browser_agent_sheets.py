import os
import asyncio
from datetime import datetime
import json
import gspread
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials

# Gọi các thư viện thuộc Layer 3 và Layer 4 trong Stack của bạn
from browser_use import Agent
from langchain_community.chat_models import ChatLiteLLM

load_dotenv()

# =====================================================================
# 1. CẤU HÌNH GOOGLE SHEETS (LAYER 4)
# =====================================================================
print("1. Đang kết nối tới Google Sheets...")
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("google_creds.json", scopes=scopes)
client = gspread.authorize(creds)

# CHÚ Ý: Hãy thay chuỗi ID dưới đây bằng ID file Google Sheets thực tế của bạn
SPREADSHEET_ID = "ĐIỀN_ID_GOOGLE_SHEET_CỦA_BẠN_VÀO_ĐÂY" 
sheet = client.open_by_key(SPREADSHEET_ID).sheet1


# =====================================================================
# 2. KHỞI TẠO NÃO BỘ AI QUA LITELLM (LAYER 3)
# =====================================================================
# Sử dụng model Llama 3.3 tiêu chuẩn thông qua router LiteLLM
llm = ChatLiteLLM(model="groq/llama-3.3-70b-versatile", temperature=0.2)


# =====================================================================
# 3. KỊCH BẢN ĐIỀU KHIỂN AGENT CÀO DATA (LAYER 4)
# =====================================================================
async def main():
    # Định nghĩa nhiệm vụ bằng tiếng Anh để AI điều khiển trình duyệt chính xác nhất
    task_prompt = (
        "Go to 'https://www.soompi.com/category/music'. "
        "Look at the latest trending or newest K-pop news articles. "
        "Extract the top 3 articles. For each article, get: "
        "1) The Title of the article, "
        "2) The short description or main group mentioned (e.g., NewJeans, BLACKPINK, BabyMonster), "
        "3) The direct URL link. "
        "Format the final answer strictly as a JSON list of lists like this: "
        '[["Title 1", "Group/Desc 1", "URL 1"], ["Title 2", "Group/Desc 2", "URL 2"]] '
        "Do not include any markdown formatting like ```json or extra explanations, just the raw JSON list."
    )
    
    print("2. Đang thả Robot Browser-use vào môi trường mạng để cào tin tức K-pop...")
    agent = Agent(task=task_prompt, llm=llm)
    
    # Kích hoạt trình duyệt ảo chạy ngầm
    history = await agent.run()
    
    # Lấy kết quả văn bản cuối cùng mà AI trích xuất được
    raw_result = history.final_result()
    print(f"-> AI trích xuất thành công dữ liệu thô: {raw_result}")
    
    # =====================================================================
    # 4. XỬ LÝ DỮ LIỆU VÀ LƯU VÀO GOOGLE SHEETS
    # =====================================================================
    print("3. Đang xử lý cấu trúc dữ liệu và đẩy lên Google Sheets...")
    try:
        # Ép kiểu chuỗi văn bản từ AI trả về thành mảng Python dữ liệu chuẩn
        articles = json.loads(raw_result)
        
        current_date = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        for article in articles:
            # Cấu trúc dòng dữ liệu: [Thời gian, Tiêu đề, Nhóm nhạc/Mô tả, Đường link]
            row_to_insert = [current_date] + article
            sheet.append_row(row_to_insert)
            
        print("🎉 THÀNH CÔNG RỰC RỠ: Tất cả tin tức K-pop mới nhất đã được nạp vào Sheets!")
        
    except Exception as e:
        print(f"⚠️ Lỗi xử lý định dạng dữ liệu: {e}")
        # Phương án dự phòng: Nếu AI trả về chuỗi text không đúng chuẩn JSON, lưu nguyên văn vào 1 ô để không mất data
        sheet.append_row([datetime.now().strftime("%d/%m/%Y %H:%M"), "Lỗi định dạng JSON - Data thô:", raw_result, ""])

if __name__ == "__main__":
    asyncio.run(main())
