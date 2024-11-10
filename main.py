from flask import Flask, request, session, redirect, url_for, render_template_string
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

data_file = 'approvals.json'

# HTML Templates
approval_pending_html = """
<!DOCTYPE html>
<html>
<head><title>Approval Pending</title></head>
<body>
    <h2>Your approval is pending. Please wait for admin review.</h2>
    <p>If you are the admin, <a href="{{ url_for('admin_login') }}">click here to enter the admin panel</a> and manage approvals.</p>
</body>
</html>
"""

welcome_html = """
<!DOCTYPE html>
<html>
<head><title>Welcome</title></head>
<body>
    <h2>Welcome, dear user! You are approved. <a href="https://herf-2-faizu-apk.onrender.com/">Visit</a></h2>
</body>
</html>
"""

admin_login_html = """
<!DOCTYPE html>
<html>
<head><title>Admin Login</title></head>
<body>
    <h2>Enter Admin Password</h2>
    <form method="POST" action="{{ url_for('admin_panel') }}">
        <input type="password" name="password" placeholder="Enter Password"/>
        <button type="submit">Login</button>
    </form>
</body>
</html>
"""

admin_panel_html = """
<!DOCTYPE html>
<html>
<head><title>Admin Panel</title></head>
<body>
    <h2>Admin Panel</h2>
    <ul>
    {% for name, details in approvals.items() %}
        <li>
            {{ name }} - Status: {{ details['status'] }}
            {% if details['status'] == 'pending' %}
                <form method="POST" action="{{ url_for('approve_user') }}">
                    <input type="hidden" name="user_name" value="{{ name }}">
                    <button type="submit">Approve</button>
                </form>
            {% endif %}
        </li>
    {% endfor %}
    </ul>
</body>
</html>
"""

# Helper function to load approval data
def load_approvals():
    if not os.path.exists(data_file):
        with open(data_file, 'w') as file:
            json.dump({}, file)
    with open(data_file, 'r') as file:
        return json.load(file)

# Helper function to save approval data
def save_approvals(data):
    with open(data_file, 'w') as file:
        json.dump(data, file)

@app.route('/')
def index():
    user_name = request.args.get('name')
    if user_name:
        session['user_name'] = user_name
        approvals = load_approvals()
        
        # Check if the user is approved and redirect to the welcome page if they are
        if user_name in approvals and approvals[user_name]['status'] == 'approved':
            return redirect(url_for('welcome'))
        else:
            return redirect(url_for('pending'))
    return "Please provide a user name in the URL, e.g., /?name=yourname"

@app.route('/pending')
def pending():
    user_name = session.get('user_name')
    approvals = load_approvals()
    
    # If the user is approved, redirect to the welcome page
    if user_name in approvals and approvals[user_name]['status'] == 'approved':
        return redirect(url_for('welcome'))
    
    return render_template_string(approval_pending_html)

@app.route('/welcome')
def welcome():
    return render_template_string(welcome_html)

@app.route('/admin/login')
def admin_login():
    return render_template_string(admin_login_html)

@app.route('/admin', methods=['POST'])
def admin_panel():
    password = request.form.get('password')
    if password == "THE FAIZU":
        approvals = load_approvals()
        return render_template_string(admin_panel_html, approvals=approvals)
    else:
        return "Incorrect password", 403

@app.route('/admin/approve', methods=['POST'])
def approve_user():
    user_name = request.form.get('user_name')
    approvals = load_approvals()
    
    # Approve the user and save the data
    if user_name in approvals:
        approvals[user_name]['status'] = 'approved'
    else:
        approvals[user_name] = {'status': 'approved'}
    
    save_approvals(approvals)
    return redirect(url_for('admin_panel'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
