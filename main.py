from flask import Flask, render_template_string, request, redirect, url_for
import json
import os

app = Flask(__name__)

# File to store user data and approvals
data_file = 'approvals.json'

# Initialize the data file if not exists
if not os.path.exists(data_file):
    with open(data_file, 'w') as file:
        json.dump({}, file)

# Route for the Home page (User enters name)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        
        # Load existing data
        with open(data_file, 'r') as file:
            data = json.load(file)
        
        # Check if name already exists
        if name in data and data[name]['status'] == 'pending':
            return render_template_string(approval_pending_html)
        elif name in data and data[name]['status'] == 'approved':
            return render_template_string(welcome_html)
        else:
            # New user, store in the database with 'pending' status
            data[name] = {'status': 'pending'}
            with open(data_file, 'w') as file:
                json.dump(data, file)
            return render_template_string(approval_pending_html)

    return render_template_string(index_html)

# Route for Admin Panel (to approve/reject)
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    password = 'THE FAIZU'
    if request.method == 'POST':
        entered_password = request.form['password']
        
        if entered_password == password:
            with open(data_file, 'r') as file:
                data = json.load(file)
            
            return render_template_string(admin_panel_html, data=data)
        else:
            return 'Incorrect Password'

    return render_template_string(admin_login_html)

# Admin accepts or rejects the request
@app.route('/approve/<name>', methods=['GET'])
def approve(name):
    with open(data_file, 'r') as file:
        data = json.load(file)
    
    if name in data and data[name]['status'] == 'pending':
        data[name]['status'] = 'approved'
        with open(data_file, 'w') as file:
            json.dump(data, file)
    
    return render_template_string(welcome_html)

@app.route('/reject/<name>', methods=['GET'])
def reject(name):
    with open(data_file, 'r') as file:
        data = json.load(file)
    
    if name in data:
        del data[name]
        with open(data_file, 'w') as file:
            json.dump(data, file)
    
    return redirect(url_for('index'))

# HTML Templates
index_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Faizu APK Approval</title>
</head>
<body>
    <h2>Enter Your Name</h2>
    <form method="post">
        <input type="text" name="name" placeholder="Enter your name" required>
        <button type="submit">Submit</button>
    </form>
</body>
</html>
'''

approval_pending_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Approval Pending</title>
</head>
<body>
    <h2>Hello, your approval is pending. Please wait.</h2>
    <p>Your request is being reviewed by the admin.</p>
    <p>If you are the admin, <a href="/admin">click here to enter the admin panel</a> and approve/reject.</p>
</body>
</html>
'''

welcome_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to Faizu APK</title>
</head>
<body>
    <h2>Welcome Dear, you are approved!</h2>
    <p>Now you can visit the APK with full access.</p>
    <a href="https://www.facebook.com/The.drugs.ft.chadwick.67" target="_blank">Visit</a>
</body>
</html>
'''

admin_login_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Login</title>
</head>
<body>
    <h2>Enter Password to Access Admin Panel</h2>
    <form method="post">
        <input type="password" name="password" placeholder="Enter password" required>
        <button type="submit">Submit</button>
    </form>
</body>
</html>
'''

admin_panel_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Panel</title>
</head>
<body>
    <h2>Admin Panel</h2>
    <h3>Pending Approval Requests</h3>
    <ul>
        {% for name, details in data.items() %}
            {% if details['status'] == 'pending' %}
                <li>
                    {{ name }} - <a href="/approve/{{ name }}">Approve</a> | <a href="/reject/{{ name }}">Reject</a>
                </li>
            {% endif %}
        {% endfor %}
    </ul>
</body>
</html>
'''

# Run the app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
