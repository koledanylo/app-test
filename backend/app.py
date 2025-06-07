import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader
import smtplib
from email.mime.text import MIMEText

# Load environment variables
load_dotenv()

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

# Email config
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# Initialize app
app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload_file():
    print("Received upload request") 
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Upload to Cloudinary
        upload_result = cloudinary.uploader.upload(file)
        file_url = upload_result['secure_url']

        # Send the email
        send_email(file.filename, file_url)

        return jsonify({'message': 'File uploaded successfully', 'url': file_url})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def send_email(filename, file_url):
    subject = "New File Uploaded"
    body = f"A new file was uploaded: {filename}\n\nDownload it here: {file_url}"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)

if __name__ == '__main__':
    app.run(debug=True)
