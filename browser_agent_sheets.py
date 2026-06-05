import os
import gspread
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials

load_dotenv()

print("1. Bắt đầu kết nối bảo mật với Google Sheets...")
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("google_creds.json", scopes=scopes)
client = gspread.authorize(creds)

# CHÚ Ý: Điền lại ID Google Sheets của bạn vào đây nhé
SPREADSHEET_ID = "1r_5sg4wKYGJw3ESFOE7vRRfkYGV2wJdGnA2ONQUOAyk" 
sheet = client.open_by_key(SPREADSHEET_ID).sheet1

print("2. Đã kết nối thành công! Bắt đầu ghi dữ liệu...")

def save_to_sheet(data_row):
    sheet.append_row(data_row)
    print("3. THÀNH CÔNG: Đã thêm một dòng mới vào Google Sheets!")

# Dòng code dưới đây đã được XÓA DẤU # để Robot thực thi hành động ghi
save_to_sheet(["Hệ thống hoàn hảo", "Robot đã thức giấc", "Sẵn sàng cào web Browser-use"])
