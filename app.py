from flask import Flask, render_template, request, send_from_directory
from email import policy
from email.parser import BytesParser
import os
import tempfile

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ATTACHMENT_FOLDER = 'static/attachments'  # Flask 的靜態目錄
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ATTACHMENT_FOLDER'] = ATTACHMENT_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(ATTACHMENT_FOLDER, exist_ok=True)

def parse_eml(file_path):
    """ 解析 EML 檔案，提取郵件資訊 """
    with open(file_path, 'rb') as f:
        msg = BytesParser(policy=policy.default).parse(f)

    subject = msg['subject']
    sender = msg['from']
    recipient = msg['to']

    content = None
    raw_content = None

    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == 'text/plain':
                content = part.get_payload(decode=True).decode(errors="ignore")
            elif content_type == 'text/html':
                raw_content = part.get_payload(decode=True).decode(errors="ignore")
    else:
        content_type = msg.get_content_type()
        if content_type == 'text/plain':
            content = msg.get_payload(decode=True).decode(errors="ignore")
        elif content_type == 'text/html':
            raw_content = msg.get_payload(decode=True).decode(errors="ignore")

    attachments = []
    for part in msg.iter_attachments():
        filename = part.get_filename()
        if filename:
            file_path = os.path.join(ATTACHMENT_FOLDER, filename)
            with open(file_path, 'wb') as f:
                f.write(part.get_payload(decode=True))
            attachments.append(filename)

    return {
        'subject': subject,
        'sender': sender,
        'recipient': recipient,
        'content': content,
        'raw_content': raw_content,
        'attachments': attachments
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    email_data = None

    if request.method == 'POST' and 'file' in request.files:
        file = request.files['file']
        save_to_server = request.form.get('save_to_server')  # 是否勾選上傳

        if file.filename:
            if save_to_server:  
                # ✅ 存到 uploads 目錄
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(file_path)
            else:
                # ✅ 使用 tempfile 處理
                with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                    temp_file.write(file.read())
                    file_path = temp_file.name  

            email_data = parse_eml(file_path)

            if not save_to_server:
                os.unlink(file_path)  # ✅ 處理完畢後刪除暫存檔案

    return render_template('index.html', email_data=email_data)

@app.route('/download/<filename>')
def download_file(filename):
    """ 提供附件下載 """
    return send_from_directory(app.config['ATTACHMENT_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
