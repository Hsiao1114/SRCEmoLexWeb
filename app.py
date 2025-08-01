# 導入必要的函式庫
from flask import Flask, render_template, request, jsonify
from collections import defaultdict, Counter
import os, re
from werkzeug.utils import secure_filename
from docx import Document

# 初始化 Flask 應用程式
app = Flask(__name__)
# 設定檔案上傳資料夾
app.config['UPLOAD_FOLDER'] = 'uploads'

# 八大情緒的列表
TARGET_EMOTIONS = ["anger", "anticipation", "disgust", "fear", "joy", "sadness", "surprise", "trust"]

# 載入情緒字典
def load_emolex(filepath):
    """
    從指定的檔案路徑載入情緒字典。
    字典格式：
    English Word\tanger\tanticipation\tdisgust\tfear\tjoy\tnegative\tpositive\tsadness\tsurprise\ttrust\tChinese-Traditional Word
    """
    emo_dict = defaultdict(list)
    try:
        with open(filepath, encoding='utf-8') as f:
            lines = f.readlines()[1:]  # 跳過標題行
            for line in lines:
                parts = line.strip().split('\t')
                # 確保行有足夠的列數
                if len(parts) >= 12:
                    emotions_str = parts[1:9]
                    chinese_word = parts[10]
                    
                    # 修正：確保 chinese_word 只包含單一字符，以符合字典設計
                    if len(chinese_word) == 1:
                        for i, val in enumerate(emotions_str):
                            if val == "1":
                                emo_dict[chinese_word].append(TARGET_EMOTIONS[i])
    except FileNotFoundError:
        print(f"錯誤：找不到檔案 {filepath}。請確認檔案路徑是否正確。")
    except Exception as e:
        print(f"載入情緒字典時發生錯誤： {e}")
    return emo_dict

# 載入字典，假設檔案位於與 app.py 相同的目錄
emo_dict = load_emolex("Chinese-Traditional-NRC-EmoLex.txt")

# 文本情緒分析邏輯
def analyze(text):
    """
    分析輸入文本的情緒。
    該函數會遍歷文本中的每個中文字符，並查詢其在情緒字典中的對應情緒。
    """
    # 修正：移除所有非中文字符，並確保是單一的中文字符
    clean_text = re.sub(r"[^\u4e00-\u9fff]", "", text)
    if not clean_text:
        return {} # 如果沒有中文字符則返回空字典
    
    # 計算總情緒分數
    emotion_count = Counter()
    for char in clean_text:
        # 查詢每個中文字符的情緒並累加分數
        for emo in emo_dict.get(char, []):
            emotion_count[emo] += 1
    
    # 將結果轉換為字典並返回
    return dict(emotion_count)

# 主頁面路由，渲染 index.html
@app.route('/')
def index():
    return render_template('index.html')

# 檔案上傳和分析路由
@app.route('/analyze', methods=['POST'])
def analyze_text_or_file():
    """
    處理來自前端的 POST 請求。
    它會檢查請求中是包含檔案還是純文字，並進行對應的分析。
    """
    # 檢查是否有檔案被上傳
    if 'file' in request.files and request.files['file'].filename != '':
        file = request.files['file']
        filename = secure_filename(file.filename)
        
        # 確保檔案為 .docx 或 .txt
        if not (filename.endswith('.docx') or filename.endswith('.txt')):
            return jsonify({"error": "不支援的檔案格式，請上傳 .docx 或 .txt 檔案。"}), 400

        # 確保上傳資料夾存在
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        full_text = ""
        try:
            if filename.endswith('.docx'):
                doc = Document(filepath)
                for para in doc.paragraphs:
                    full_text += para.text
            elif filename.endswith('.txt'):
                with open(filepath, 'r', encoding='utf-8') as f:
                    full_text = f.read()

            result = analyze(full_text)
            
            if not result:
                return jsonify({"message": "文件中沒有找到任何情緒詞。"}), 200

            return jsonify(result)

        except Exception as e:
            return jsonify({"error": f"檔案處理時發生錯誤: {str(e)}"}), 500
        finally:
            # 確保檔案被刪除
            if os.path.exists(filepath):
                os.remove(filepath)
    
    # 如果沒有檔案，檢查是否有文字輸入
    elif 'text' in request.form and request.form['text'].strip() != '':
        full_text = request.form['text']
        result = analyze(full_text)

        if not result:
            return jsonify({"message": "輸入的文字中沒有找到任何情緒詞。"}), 200
        
        return jsonify(result)

    # 如果既沒有檔案也沒有文字
    return jsonify({"error": "請輸入文字或選擇一個檔案。"}), 400

# 應用程式入口點
if __name__ == '__main__':
    # 啟動應用程式，並啟用偵錯模式
    app.run(debug=True)
