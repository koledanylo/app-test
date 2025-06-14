import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader
import smtplib
from email.mime.text import MIMEText

# Load environment variables from .env
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

# Email configuration
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


# Upload endpoint
@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        print("📤 Upload request received")

        if 'file' not in request.files:
            print("⚠️ No file part in request")
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']

        if file.filename == '':
            print("⚠️ Empty filename received")
            return jsonify({'error': 'No selected file'}), 400

        # ✅ Upload to Cloudinary as a raw (non-image) file
        upload_result = cloudinary.uploader.upload(
            file,
            resource_type="auto",         # Required for PDFs and other files
            type="upload",               # Default type
            access_mode="public",        # Ensure file is publicly accessible
            format="pdf"                 # Optional: force PDF extension
        )

        file_url = upload_result['url']
        print(f"✅ File uploaded successfully: {file_url}")

        # Send notification email
        send_email(file.filename, file_url)
        print("📧 Email notification sent")

        return jsonify({'message': 'Success', 'url': file_url})

    except Exception as e:
        import traceback
        traceback.print_exc()
        print("❌ Upload failed:", e)
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


# Send email with link
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


# Start Flask app
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
