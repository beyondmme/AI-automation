import os
from dotenv import load_dotenv
import litellm

load_dotenv()

if not os.getenv("GROQ_API_KEY"):
    raise ValueError("Rủi ro: Không tìm thấy GROQ_API_KEY! Hãy kiểm tra lại file .env")

print(" Đang gửi yêu cầu tới model Llama 3.3 mới...")

try:
    response = litellm.completion(
        # Đổi tên model cũ sang model mới này:
        model="groq/llama-3.3-70b-versatile", 
        messages=[{"role": "user", "content": "Xin chào, bạn là AI Agent chạy qua LiteLLM đúng không?"}]
    )
    print("\n AI phản hồi thành công:")
    print(response.choices[0].message.content)
except Exception as e:
    print(f"Có lỗi xảy ra: {e}")