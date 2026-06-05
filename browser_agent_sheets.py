import os
import asyncio
from datetime import datetime
import json
import gspread
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials

# Sử dụng kết nối trực tiếp và chuẩn xác nhất cho Groq và Browser-use
from browser_use import Agent
from langchain_groq import ChatGroq

load_dotenv()

# =====================================================================
# 1. CẤU HÌNH GOOGLE SHEETS
# =====================================================================
print("1. Đang kết nối tới hệ thống Google Sheets...")
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("google_creds.json", scopes=scopes)
client = gspread.authorize(creds)

# ID bảng tính của bạn đã được cấu hình cố định chuẩn xác
SPREADSHEET_ID = "1r_5sg4wKYGJw3ESFOE7vRRfkYGV2wJdGnA2ONQUOAyk" 
sheet = client.open_by_key(SPREADSHEET_ID).sheet1


# =====================================================================
# 2. KHỞI TẠO NÃO BỘ LLAMA 3 CỦA GROQ
# =====================================================================
print("2. Đang nạp cấu hình API Groq cho Llama 3...")
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.3)


# =====================================================================
# 3. KỊCH BẢN ĐIỀU KHIỂN AGENT SĂN TIN TỨC FEMALE K-POP
# =====================================================================
async def main():
    task_prompt = """
    1. Open 'https://www.soompi.com/category/music' and scan the latest K-pop news articles.
    2. Focus primarily on articles related to female K-pop groups, female idols, or general industry trends that impact female artists.
    3. Cover all relevant categories such as: Comebacks, Music Records, Brand Strategy, or Creative Concepts.
    4. Extract the top 5 most critical or trending news items. For each item, capture:
       - The Article Title.
       - The Specific Category (e.g., Comeback, Music Record, Fashion/Branding, Agency Strategy, Concept).
       - A concise summary identifying the key female artists involved (e.g., NewJeans, BLACKPINK, BabyMonster, aespa, IVE, etc.) and what happened.
       - The direct URL link.
    5. Output the final result strictly as a raw JSON list of lists (WITHOUT using markdown code blocks like ```json), following this format:
    [["Title 1", "Category 1", "Summary 1", "URL 1"], ["Title 2", "Category 2", "Summary 2", "URL 2"]]
    """
    
    print("3. Đang kích hoạt Browser-use đi săn lùng tin tức Female K-pop toàn diện...")
    agent = Agent(task=task_prompt, llm=llm)
    
    # Kích hoạt robot quét dữ liệu ngầm
    history = await agent.run()
    raw_result = history.final_result()
    print(f"-> Dữ liệu thô AI trích xuất được: {raw_result}")
    
    # =====================================================================
    # 4. ĐẨY DATA VÀO GOOGLE SHEETS
    # =====================================================================
    print("4. Đang xử lý cấu trúc dữ liệu và ghi vào Google Sheets...")
    try:
        articles = json.loads(raw_result)
        current_date = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        for article in articles:
            # Định dạng dòng: [Thời gian quét, Tiêu đề, Phân loại, Tóm tắt/Nghệ sĩ, Link gốc]
            row_to_insert = [current_date] + article
            sheet.append_row(row_to_insert)
            
        print("🎉 THÀNH CÔNG: Toàn bộ dữ liệu Female K-pop toàn diện đã được cập nhật vào Sheets!")
        
    except Exception as e:
        print(f"⚠️ Lỗi định dạng dữ liệu: {e}")
        sheet.append_row([datetime.now().strftime("%d/%m/%Y %H:%M"), "Lỗi định dạng - Dữ liệu thô từ AI:", raw_result, "", ""])

if __name__ == "__main__":
    asyncio.run(main())
