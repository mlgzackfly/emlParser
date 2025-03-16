# 📩 EML Parser Tool

This is a simple **Flask-based EML parser tool** that allows users to:
✅ Extract **subject, sender, recipient, and content** from `.eml` files  
✅ **Format and display raw HTML content**  
✅ **Download email attachments**  
✅ Choose whether to **save the file to the server** or process it temporarily  

---

## 🚀 Installation & Setup

### **1. Install dependencies**
Ensure you have Python 3 installed, then run:
```bash
pip install -r requirements.txt
```

### **2. Start the Flask server**
```bash
python app.py
```

### **3. Use the tool**
Open your browser and go to:
```
http://127.0.0.1:5000/
```
Upload an `.eml` file to parse its contents.

---

## 🛠 Features

### ✅ 1. Extract email metadata
- Retrieve **subject, sender, and recipient**
- Extract **plain text content**
- Format and display **raw HTML content**

### ✅ 2. Download attachments
- Identify and list all **email attachments**
- Click to download extracted files

### ✅ 3. Choose whether to save `.eml`
- **Checked "Save to Server"** → Stores in `/uploads`
- **Unchecked** → Uses **temporary processing**, avoiding long-term storage

---

## 🎨 UI Preview
🔹 **Clean and simple UI, powered by Tailwind CSS**  
![EML Parser UI](https://via.placeholder.com/800x400?text=EML+Parser+UI)

---

## 🔥 Future Improvements
- [ ] **API support** for integration with other applications
- [ ] **Support for additional email formats**
- [ ] **Enhanced security (XSS protection, input validation, etc.)**

---

## 📜 License
MIT License
