import os
import asyncio
from datetime import datetime

import gspread
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
from langchain_openai import ChatOpenAI  # ← FIX: dùng ChatOpenAI thay ChatGroq
from browser_use import Agent

# ============================================================
# BƯỚC 0: Nạp biến môi trường từ file .env (local)
#         hoặc từ GitHub Secrets (khi chạy trên cloud)
# ============================================================
load_dotenv()

# Kiểm tra key bắt buộc
for key in ["GROQ_API_KEY", "SPREADSHEET_ID"]:
    if not os.getenv(key):
        raise ValueError(f"❌ Thiếu biến môi trường: {key}. Kiểm tra file .env hoặc GitHub Secrets.")

# ============================================================
# BƯỚC 1: Kết nối Google Sheets qua Service Account
# ============================================================
print("1. Đang kết nối tới Google Sheets...")

scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("google_creds.json", scopes=scopes)
client = gspread.authorize(creds)

SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
sheet = client.open_by_key(SPREADSHEET_ID).sheet1
print("   ✅ Kết nối Google Sheets thành công!")

# ============================================================
# BƯỚC 2: Khởi tạo LLM
#
# FIX QUAN TRỌNG: browser-use yêu cầu LLM có thuộc tính .provider
# ChatGroq KHÔNG có thuộc tính này → lỗi AttributeError
# ChatOpenAI CÓ thuộc tính này → hoạt động đúng
#
# Groq cung cấp endpoint tương thích OpenAI, nên ta dùng
# ChatOpenAI và trỏ base_url vào Groq là xong.
# ============================================================
print("2. Đang nạp cấu hình LLM (Groq via OpenAI-compatible endpoint)...")

llm = ChatOpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile",  # model mạnh nhất trên Groq free
    temperature=0.3,
)
print("   ✅ LLM sẵn sàng!")

# ============================================================
# BƯỚC 3: Hàm tiện ích lưu dữ liệu vào Sheet
# ============================================================
def save_to_sheet(data_row: list):
    """Ghi một dòng dữ liệu vào cuối Google Sheet."""
    sheet.append_row(data_row)
    print(f"   ✅ Đã lưu vào Sheet: {data_row}")

# ============================================================
# BƯỚC 4: Task cho AI Agent
# Thay đổi task_prompt để scrape bất kỳ nội dung nào bạn muốn
# ============================================================
TASK_PROMPT = """
Hãy vào trang web https://www.melon.com/chart/index.htm và lấy thông tin 
top 5 bài hát đang đứng đầu bảng xếp hạng Melon hiện tại.

Trả về danh sách gồm 5 dòng, mỗi dòng theo định dạng chính xác:
RANK | SONG_TITLE | ARTIST_NAME

Chỉ trả về dữ liệu, không cần giải thích thêm.
"""

# ============================================================
# BƯỚC 5: Chạy Agent
# ============================================================
async def main():
    print("3. Đang kích hoạt Browser-use Agent...")

    agent = Agent(
        task=TASK_PROMPT,
        llm=llm,
        use_vision=False,  # tắt vision để tiết kiệm token trên free tier
    )

    result = await agent.run()

    # Lấy nội dung kết quả cuối cùng
    final_text = result.final_result() if hasattr(result, "final_result") else str(result)
    print(f"\n   Agent trả về:\n{final_text}\n")

    # Lưu vào Google Sheets
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M UTC")
    save_to_sheet([timestamp, "Melon Top 5 Chart", final_text])

    print("✅ Hoàn thành toàn bộ pipeline!")


if __name__ == "__main__":
    asyncio.run(main())
