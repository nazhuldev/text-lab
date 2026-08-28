# 🧪 Text Lab

App nhỏ dùng Python (Flask) để xử lý văn bản: **dịch thuật**, **tóm tắt**, và **phân tích cảm xúc** - tất cả trong một giao diện web đơn giản, gọn gàng.

## ✨ Tính năng

- 🌐 **Dịch thuật** — dịch văn bản qua nhiều ngôn ngữ (Anh, Việt, Nhật, Hàn, Trung, Pháp...)
- ✂️ **Tóm tắt văn bản** — rút gọn đoạn văn dài thành các câu quan trọng nhất
- 🎭 **Phân tích cảm xúc** — đoán văn bản mang sắc thái tích cực, tiêu cực hay trung lập

## 🛠️ Công nghệ sử dụng

- **Backend:** Python, Flask
- **Dịch thuật:** [deep-translator](https://pypi.org/project/deep-translator/)
- **Tóm tắt & cảm xúc:** thuật toán tự viết (rule-based, chạy offline)
- **Frontend:** HTML, CSS, JavaScript thuần

## 🚀 Cài đặt & chạy thử

```bash
# 1. Cài thư viện cần thiết
pip install -r requirements.txt

# 2. Chạy server
python app.py

# 3. Mở trình duyệt vào
http://localhost:5000
```

## 📁 Cấu trúc project

```
text-lab/
├── app.py                  # Backend Python (Flask) - xử lý logic
├── templates/
│   └── index.html          # Giao diện web (HTML/CSS/JS)
├── requirements.txt        # Danh sách thư viện cần cài
└── README.md
```

## 📝 Cách hoạt động

- **Tóm tắt:** đếm tần suất từ xuất hiện trong bài, câu nào chứa nhiều từ quan trọng thì được giữ lại (thuật toán extractive summarization).
- **Phân tích cảm xúc:** so sánh số từ tích cực và tiêu cực trong câu dựa trên từ điển có sẵn — cách đơn giản, dễ hiểu, không cần model AI nặng.
- **Dịch thuật:** dùng Google Translate miễn phí qua thư viện `deep-translator`.

---

Made with 🐍 by [Kyu Dev](https://github.com/nazhuldev)
