from flask import Flask, request, redirect, jsonify, render_template_string
import uuid
import os

app = Flask(__name__)

# یوزر کی unique key کو فائل میں اسٹور کریں
def get_or_create_user_key():
    if os.path.exists("user_key.txt"):
        with open("user_key.txt", "r") as file:
            unique_key = file.read().strip()
    else:
        unique_key = str(uuid.uuid4())
        with open("user_key.txt", "w") as file:
            file.write(unique_key)
    return unique_key

# یوزر کے اپروول اسٹیٹس کو چیک کریں
def is_approved(unique_key):
    if os.path.exists("approved_requests.txt"):
        with open("approved_requests.txt", "r") as file:
            approved_keys = file.read().splitlines()
            return unique_key in approved_keys
    return False

# یوزر کا پیج جہاں وہ اپنی unique key چیک کرے گا
@app.route('/request_approval', methods=['GET'])
def request_approval():
    unique_key = get_or_create_user_key()
    
    # اگر یوزر کا اپروول ہو چکا ہے تو براہ راست لنک پر ری ڈائریکٹ کریں
    if is_approved(unique_key):
        return redirect("https://mone-56u0.onrender.com")
    
    # اگر اپروول ابھی تک نہ ہوا ہو تو اپروول پیج ظاہر کریں
    return render_template_string('''
        <h2>Your unique key:</h2>
        <p>{{ key }}</p>
        <form action="/send_request" method="post">
            <input type="hidden" name="unique_key" value="{{ key }}">
            <button type="submit">Send Approval Request</button>
        </form>
    ''', key=unique_key)

# اپروول کی درخواست بھیجیں
@app.route('/send_request', methods=['POST'])
def send_request():
    unique_key = get_or_create_user_key()
    
    # اگر اپروول کی درخواست پہلے سے موجود نہیں تو اسے اسٹور کریں
    if not os.path.exists("approval_requests.txt") or unique_key not in open("approval_requests.txt").read():
        with open("approval_requests.txt", "a") as file:
            file.write(f"{unique_key}\n")
    
    return jsonify({"message": "Approval request sent successfully", "key": unique_key})

if __name__ == '__main__':
    app.run(port=5000)
