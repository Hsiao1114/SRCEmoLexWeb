# SRCEmoLexWeb
# 中文情緒分析工具（基於 NRC 字典）

本專案是一個使用 Python + Flask 搭配 JavaScript/HTML/CSS 製作的情緒分析網頁應用，支援使用者輸入中文文章或上傳 `.txt` / `.docx` 檔案，分析其情緒屬性（八大情緒），並輸出分析結果。

## 🔍 專案特色

- ✅ 支援手動輸入文章或檔案上傳
- ✅ 使用 [NRC Emotion Lexicon（繁體中文版本）](http://saifmohammad.com/WebPages/NRC-Emotion-Lexicon.htm)
- ✅ 支援 `.txt` 與 `.docx` 檔案格式
- ✅ 輕量前後端分離架構
- ✅ 分析結果清楚列出八大情緒的次數與比例

---

## 📂 專案結構

```

SRCEmoLexWeb/
├── app.py                               # Flask 後端主程式
├── Chinese-Traditional-NRC-EmoLex.txt   # 情緒字典（繁體中文）
├── templates/
│   └── index.html                       # 前端 HTML 介面
├── static/
│   └── style.css                        # CSS 樣式
└── uploads/                             # 檔案上傳暫存資料夾（自動建立）

````

---

## 🚀 快速啟動

### 1️⃣ 安裝環境

建議使用 Python 3.8+
```bash
pip install flask python-docx
````

### 2️⃣ 執行後端伺服器

```
python app.py
```

啟動後開啟瀏覽器，進入：

```
http://127.0.0.1:5000/
```

即可看到情緒分析網頁。

---

## 🖥 使用方式

### ✅ 方式一：手動輸入文章

1. 在頁面文字框中貼上中文文章內容
2. 點選「分析情緒」按鈕
3. 系統會顯示各情緒出現次數與比例

### ✅ 方式二：上傳文字檔案

1. 點選「選擇檔案」按鈕
2. 上傳 `.txt` 或 `.docx` 文件
3. 點選「分析情緒」按鈕查看結果

---

## 📊 支援的八大情緒分類

根據 NRC 字典，此系統可偵測以下情緒：

* 😠 anger（憤怒）
* 🌱 anticipation（期待）
* 🤢 disgust（厭惡）
* 😨 fear（恐懼）
* 😊 joy（喜悅）
* 😢 sadness（悲傷）
* 😲 surprise（驚訝）
* 🤝 trust（信任）

---

## 🧠 核心邏輯

* 載入繁體中文 NRC 字典，建立字詞→情緒對應表
* 分析輸入文字中所有中文字符
* 統計每個字符出現次數，對應情緒總和
* 計算各情緒的總出現次數與百分比

---

## 📝 備註

* 若使用 `docx` 檔案，系統會使用 `python-docx` 模組解析段落內容。
* 若字典檔案有更新，請確保格式與 `Chinese-Traditional-NRC-EmoLex.txt` 相同。

---

## 📜 授權與引用

本專案為學術與學習用途，可自由修改與擴充。

情緒字典來自：

> Mohammad, Saif M. and Turney, Peter D. (2013), “Crowdsourcing a Word-Emotion Association Lexicon.” Computational Intelligence, 29(3): 436–465.

---

## 🤝 貢獻與聯繫

歡迎提出 issue、fork 本專案或提交 pull request。

若你覺得有幫助，歡迎點個 ⭐️！

```


