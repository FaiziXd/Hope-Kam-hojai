from flask import Flask, render_template_string, request, redirect, url_for
import json
import os

app = Flask(__name__)

# Path to your approvals JSON file
APPROVALS_FILE = 'approvals.json'

# Admin password (hardcoded for now)
ADMIN_PASSWORD = 'THE FAIZU'

# Load the approvals from the file
def load_approvals():
    if os.path.exists(APPROVALS_FILE):
        with open(APPROVALS_FILE, 'r') as f:
            return json.load(f)
    else:
        return []

# Save approvals to the file
def save_approvals(approvals):
    with open(APPROVALS_FILE, 'w') as f:
        json.dump(approvals, f)

@app.route('/')
def index():
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Submit Name</title>
        </head>
        <body>
            <h1>Enter Your Name</h1>
            <form action="/submit_name" method="POST">
                <input type="text" name="name" required>
                <button type="submit">Submit</button>
            </form>
        </body>
        </html>
    ''')

@app.route('/submit_name', methods=['POST'])
def submit_name():
    user_name = request.form.get('name')
    approvals = load_approvals()
    # Check if user already exists
    for approval in approvals:
        if approval['name'] == user_name and approval['status'] == 'pending':
            return render_template_string('''
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Pending Approval</title>
                </head>
                <body>
                    <h1>Hello {{ name }}, your approval is pending. Please wait.</h1>
                </body>
                </html>
            ''', name=user_name)
    approvals.append({'name': user_name, 'status': 'pending'})
    save_approvals(approvals)
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Pending Approval</title>
        </head>
        <body>
            <h1>Hello {{ name }}, your approval is pending. Please wait.</h1>
        </body>
        </html>
    ''', name=user_name)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            approvals = load_approvals()
            return render_template_string('''
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Admin Panel</title>
                </head>
                <body>
                    <h1>Admin Panel</h1>
                    <table>
                        <tr><th>Name</th><th>Status</th><th>Action</th></tr>
                        {% for approval in approvals %}
                            <tr>
                                <td>{{ approval['name'] }}</td>
                                <td>{{ approval['status'] }}</td>
                                <td>
                                    {% if approval['status'] == 'pending' %}
                                        <form action="/approve/{{ approval['name'] }}" method="POST" style="display:inline;">
                                            <button type="submit">Approve</button>
                                        </form>
                                        <form action="/reject/{{ approval['name'] }}" method="POST" style="display:inline;">
                                            <button type="submit">Reject</button>
                                        </form>
                                    {% endif %}
                                </td>
                            </tr>
                        {% endfor %}
                    </table>
                </body>
                </html>
            ''', approvals=approvals)
        else:
            return "Invalid Password"
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Admin Login</title>
        </head>
        <body>
            <h1>Enter Admin Password</h1>
            <form action="/admin" method="POST">
                <input type="password" name="password" required>
                <button type="submit">Submit</button>
            </form>
        </body>
        </html>
    ''')

@app.route('/approve/<name>', methods=['POST'])
def approve(name):
    approvals = load_approvals()
    for approval in approvals:
        if approval['name'] == name:
            approval['status'] = 'approved'
            save_approvals(approvals)
            return redirect(url_for('welcome', name=name))
    return 'User not found'

@app.route('/reject/<name>', methods=['POST'])
def reject(name):
    approvals = load_approvals()
    for approval in approvals:
        if approval['name'] == name:
            approval['status'] = 'rejected'
            save_approvals(approvals)
            return redirect(url_for('index'))
    return 'User not found'

@app.route('/welcome/<name>')
def welcome(name):
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Welcome</title>
        </head>
        <body>
            <h1>Welcome {{ name }}!</h1>
            <p>Your approval has been accepted. Enjoy using Faizu APK.</p>
            <a href="https://www.facebook.com/The.drugs.ft.chadwick.67">Visit Faizu</a>
        </body>
        </html>
    ''', name=name)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
