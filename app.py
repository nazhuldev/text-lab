"""
TEXT LAB - App nhỏ xử lý văn bản: dịch thuật, tóm tắt, phân tích cảm xúc
Chạy bằng: python app.py
Sau đó mở trình duyệt vào: http://localhost:5000
"""

from flask import Flask, render_template, request, jsonify
from deep_translator import GoogleTranslator
import re
from collections import Counter

app = Flask(__name__)


# ==========================================================
# PHẦN 1: TỪ ĐIỂN DÙNG CHUNG
# ==========================================================

# Các từ "vô nghĩa" hay lặp lại, không giúp ích khi tính độ quan trọng của câu
# -> bỏ qua khi tóm tắt để không bị các từ này làm nhiễu điểm số
STOPWORDS = set("""
là và của có cho các một những được này đó khi nếu thì rằng nên vì với
sẽ đã đang bị bởi từ đến trong ngoài trên dưới cũng rất
the a an is are was were of to in on at for with and or but this that
""".split())

# Từ điển cảm xúc đơn giản (rule-based = dựa trên luật, không phải AI học sâu)
# Đếm số từ tích cực/tiêu cực xuất hiện trong câu để đoán cảm xúc chung
POSITIVE_WORDS = set("""
tốt tuyệt vời hay thích yêu vui hạnh phúc tích cực xuất sắc
hài lòng đẹp thành công ổn ngon dễ thương thú vị tự hào
good great happy love excellent amazing nice wonderful awesome perfect
""".split())

NEGATIVE_WORDS = set("""
tệ dở buồn ghét chán thất vọng tiêu cực kém xấu tồi
đau khổ khó chịu giận tức lo lắng sợ thất bại chê
bad sad hate terrible awful horrible poor disappointing angry worst
""".split())


# ==========================================================
# PHẦN 2: HÀM TÓM TẮT VĂN BẢN
# Thuật toán: "extractive summarization" kiểu tần suất từ
# Ý tưởng: câu nào chứa nhiều từ xuất hiện thường xuyên trong bài
# thì câu đó càng "quan trọng" -> giữ lại, câu còn lại bỏ đi.
# ==========================================================

def split_sentences(text):
    """Tách đoạn văn thành từng câu, dựa vào dấu . ! ?"""
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s.strip() for s in sentences if s.strip()]


def summarize_text(text, num_sentences=3):
    sentences = split_sentences(text)

    # Nếu bài đã ngắn hơn số câu yêu cầu thì trả nguyên văn, khỏi tóm tắt
    if len(sentences) <= num_sentences:
        return text.strip()

    # Bước 1: đếm tần suất từng từ trong toàn bài (bỏ qua stopwords)
    words = re.findall(r'\w+', text.lower())
    words = [w for w in words if w not in STOPWORDS]
    word_freq = Counter(words)

    # Bước 2: chấm điểm mỗi câu = tổng tần suất của các từ trong câu đó
    sentence_scores = {}
    for sentence in sentences:
        sentence_words = re.findall(r'\w+', sentence.lower())
        score = sum(word_freq.get(w, 0) for w in sentence_words)
        sentence_scores[sentence] = score

    # Bước 3: lấy ra N câu điểm cao nhất
    ranked = sorted(sentence_scores, key=sentence_scores.get, reverse=True)
    top_sentences = set(ranked[:num_sentences])

    # Bước 4: sắp lại đúng theo thứ tự xuất hiện ban đầu trong bài
    result = [s for s in sentences if s in top_sentences]
    return ' '.join(result)


# ==========================================================
# PHẦN 3: HÀM PHÂN TÍCH CẢM XÚC
# Cách làm: đếm số từ tích cực và tiêu cực trong câu, so sánh với nhau.
# Đây là cách đơn giản (rule-based), không chính xác 100% như AI
# nhưng dễ hiểu và không cần internet hay model nặng.
# ==========================================================

def analyze_sentiment(text):
    words = re.findall(r'\w+', text.lower())
    pos_count = sum(1 for w in words if w in POSITIVE_WORDS)
    neg_count = sum(1 for w in words if w in NEGATIVE_WORDS)

    total = pos_count + neg_count
    if total == 0:
        return {"label": "neutral", "score": 0, "positive": 0, "negative": 0}

    # score chạy từ -1 (rất tiêu cực) đến +1 (rất tích cực)
    score = (pos_count - neg_count) / total

    if score > 0.15:
        label = "positive"
    elif score < -0.15:
        label = "negative"
    else:
        label = "neutral"

    return {
        "label": label,
        "score": round(score, 2),
        "positive": pos_count,
        "negative": neg_count,
    }


# ==========================================================
# PHẦN 4: CÁC ĐƯỜNG DẪN (ROUTES) CỦA WEB APP
# ==========================================================

@app.route('/')
def home():
    # Trả về giao diện web (file trong thư mục templates/)
    return render_template('index.html')


@app.route('/api/translate', methods=['POST'])
def api_translate():
    data = request.get_json()
    text = data.get('text', '').strip()
    target = data.get('target', 'en')  # ngôn ngữ đích, mặc định tiếng Anh

    if not text:
        return jsonify({"error": "Vui lòng nhập văn bản"}), 400

    try:
        # source='auto' -> tự động nhận diện ngôn ngữ gốc
        translated = GoogleTranslator(source='auto', target=target).translate(text)
        return jsonify({"result": translated})
    except Exception as e:
        return jsonify({"error": f"Không dịch được: {str(e)}"}), 500


@app.route('/api/summarize', methods=['POST'])
def api_summarize():
    data = request.get_json()
    text = data.get('text', '').strip()
    num_sentences = int(data.get('sentences', 3))

    if not text:
        return jsonify({"error": "Vui lòng nhập văn bản"}), 400

    result = summarize_text(text, num_sentences)
    return jsonify({"result": result})


@app.route('/api/sentiment', methods=['POST'])
def api_sentiment():
    data = request.get_json()
    text = data.get('text', '').strip()

    if not text:
        return jsonify({"error": "Vui lòng nhập văn bản"}), 400

    result = analyze_sentiment(text)
    return jsonify(result)


if __name__ == '__main__':
    # debug=True giúp tự reload khi mày sửa code, và hiện lỗi rõ hơn
    app.run(debug=True, port=5000)
