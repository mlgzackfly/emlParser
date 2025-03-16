from flask import Flask, render_template, request, send_file
from email import policy
from email.parser import BytesParser
import os
import io

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ATTACHMENT_FOLDER = 'static/attachments'  # Flask 靜態目錄
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ATTACHMENT_FOLDER'] = ATTACHMENT_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(ATTACHMENT_FOLDER, exist_ok=True)

def parse_eml(file, save_attachments=True):
    """ 解析 EML 檔案，提取郵件資訊 """
    msg = BytesParser(policy=policy.default).parse(file)

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
            raw_content = part.get_payload(decode=True).decode(errors="ignore")

    attachments = []
    if save_attachments:
        for part in msg.iter_attachments():
            filename = part.get_filename()
            if filename:
                file_data = part.get_payload(decode=True)
                file_io = io.BytesIO(file_data)  # 用內存儲存檔案
                attachments.append((filename, file_io))

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
        save_to_server = request.form.get('save_to_server')  # 是否勾選儲存

        if file.filename:
            # 使用內存中的檔案處理
            if save_to_server:  
                # 儲存到 uploads 目錄
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(file_path)
                with open(file_path, 'rb') as f:
                    email_data = parse_eml(f, save_attachments=True)
                os.unlink(file_path)  # 儲存後刪除檔案
            else:
                # 不儲存檔案，直接在內存中處理
                email_data = parse_eml(file, save_attachments=False)

    return render_template('index.html', email_data=email_data)

@app.route('/download/<filename>')
def download_file(filename):
    """ 提供附件下載 """
    # 提供內存中的檔案下載
    for attachment in email_data['attachments']:
        if attachment[0] == filename:
            return send_file(attachment[1], as_attachment=True, download_name=filename)
    return "File not found", 404

if __name__ == '__main__':
    app.run(debug=True)
