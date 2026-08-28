# Text Lab

App nhỏ dùng Python (Flask) xử lý văn bản: dịch thuật, tóm tắt, và phân tích cảm xúc.

## Cách chạy

1. Cài thư viện cần thiết (chỉ cần làm 1 lần):
   ```
   pip install -r requirements.txt
   ```

2. Chạy server:
   ```
   python app.py
   ```

3. Mở trình duyệt vào: **http://localhost:5000**

## Cấu trúc project

```
text-lab/
├── app.py                  # Backend Python (Flask) - xử lý logic
├── templates/
│   └── index.html          # Giao diện web (HTML/CSS/JS)
├── requirements.txt        # Danh sách thư viện cần cài
└── README.md
```

## Cách hoạt động (giải thích ngắn gọn)

- **Dịch thuật**: dùng thư viện `deep-translator` (gọi Google Translate miễn phí, không cần API key). Cần có internet.
- **Tóm tắt**: thuật toán tự viết — đếm từ nào xuất hiện nhiều nhất trong bài, câu nào chứa nhiều từ đó thì được coi là quan trọng và giữ lại. Chạy offline, không cần internet.
- **Phân tích cảm xúc**: đếm số từ tích cực/tiêu cực có trong câu (dựa vào 2 danh sách từ trong `app.py`), so sánh với nhau ra điểm số. Đây là cách đơn giản (rule-based), không phải AI học sâu, nên độ chính xác có giới hạn — câu càng dùng từ ngữ rõ ràng thì đoán càng đúng.

## Muốn sửa gì thì sửa ở đâu

- Thêm/bớt từ vào từ điển cảm xúc → sửa `POSITIVE_WORDS` và `NEGATIVE_WORDS` trong `app.py`
- Đổi ngôn ngữ dịch mặc định → sửa phần `<option>` trong `templates/index.html`
- Đổi giao diện, màu sắc → sửa phần `<style>` trong `templates/index.html`
