from flask import Flask, render_template_string, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For session tracking

# Approval data file
data_file = 'approvals.json'

# Initialize the data file if it doesn't exist
if not os.path.exists(data_file):
    with open(data_file, 'w') as file:
        json.dump({}, file)

# Route for user login
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        
        # Load approval data
        with open(data_file, 'r') as file:
            data = json.load(file)
        
        session['user_name'] = name  # Track the user in the session
        
        # Check approval status
        if name in data and data[name]['status'] == 'approved':
            session['approved'] = True  # Set session for approved users
            return redirect(url_for('welcome'))
        elif name not in data:
            # Add new user with 'pending' status
            data[name] = {'status': 'pending'}
            with open(data_file, 'w') as file:
                json.dump(data, file)
            return redirect(url_for('pending'))
        else:
            return redirect(url_for('pending'))

    return render_template_string(index_html)

# Page for pending approval
@app.route('/pending')
def pending():
    if session.get('approved'):
        return redirect(url_for('welcome'))
    return render_template_string(approval_pending_html)

# Page shown to approved users
@app.route('/welcome')
def welcome():
    user_name = session.get('user_name')
    
    # Load approval data to confirm user is approved
    with open(data_file, 'r') as file:
        data = json.load(file)
    
    if user_name in data and data[user_name]['status'] == 'approved':
        return render_template_string(welcome_html)
    else:
        return redirect(url_for('pending'))

# Admin login page
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        entered_password = request.form['password']
        
        if entered_password == 'THE FAIZU':
            # Load approval data for admin panel
            with open(data_file, 'r') as file:
                data = json.load(file)
            return render_template_string(admin_panel_html, data=data)
        else:
            return 'Incorrect Password'

    return render_template_string(admin_login_html)

# Approve user (admin only)
@app.route('/approve/<name>')
def approve(name):
    with open(data_file, 'r') as file:
        data = json.load(file)
    
    if name in data and data[name]['status'] == 'pending':
        # Update user to 'approved'
        data[name]['status'] = 'approved'
        with open(data_file, 'w') as file:
            json.dump(data, file)
    
    return redirect(url_for('admin'))

# Reject user (admin only)
@app.route('/reject/<name>')
def reject(name):
    with open(data_file, 'r') as file:
        data = json.load(file)
    
    if name in data:
        # Remove the user's entry
        del data[name]
        with open(data_file, 'w') as file:
            json.dump(data, file)
    
    return redirect(url_for('admin'))

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
    <h2>Your approval is pending. Please wait for admin review.</h2>
    <p>If you are the admin, <a href="/admin">click here to enter the admin panel</a> and manage approvals.</p>
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
    <h2>Welcome! You are approved.</h2>
    <p>You have lifetime access to the APK features.</p>
    <a href="https://www.facebook.com/The.drugs.ft.chadwick.67" target="_blank">Visit Here</a>
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
                <li>{{ name }} - <a href="/approve/{{ name }}">Approve</a> | <a href="/reject/{{ name }}">Reject</a></li>
            {% endif %}
        {% endfor %}
    </ul>
</body>
</html>
'''

# Run the app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
