from flask import Flask, request, render_template_string, redirect, url_for
import sqlite3

app = Flask(__name__)

# HTML templates
index_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Approval System</title>
</head>
<body>
    <h1>Enter your name:</h1>
    <form method="post">
        <input type="text" name="name" required>
        <button type="submit">Send Request</button>
    </form>
</body>
</html>
"""

admin_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Admin Panel</title>
</head>
<body>
    <h1>Requests:</h1>
    <ul>
    {% for request in requests %}
        <li>{{ request[1] }} ({{ request[2] }})</li>
        <form method="post" action="/admin/approve/{{ request[0] }}">
            <select name="status">
                <option value="approved">Approve</option>
                <option value="rejected">Reject</option>
            </select>
            <button type="submit">Update Status</button>
        </form>
    {% endfor %}
    </ul>
</body>
</html>
"""

visit_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Welcome!</title>
</head>
<body>
    <h1>Welcome to our platform!</h1>
    <a href="(link unavailable)" target="_blank">Visit</a>
</body>
</html>
"""

# Database connection
conn = sqlite3.connect('approval.db')
cursor = conn.cursor()

# Create table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS requests (
        id INTEGER PRIMARY KEY,
        name TEXT,
        status TEXT
    )
''')

# Close connection
conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        # Insert into database
        conn = sqlite3.connect('approval.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO requests (name, status) VALUES (?, ?)', (name, 'pending'))
        conn.commit()
        conn.close()
        return 'Request sent!'
    return render_template_string(index_template)

@app.route('/admin', methods=['GET'])
def admin_login():
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Admin Login</title>
        </head>
        <body>
            <h1>Admin Login</h1>
            <form method="post" action="/admin/login">
                <input type="password" name="password" required>
                <button type="submit">Login</button>
            </form>
        </body>
        </html>
    ''')

@app.route('/admin/login', methods=['POST'])
def admin_login_check():
    password = request.form['password']
    if password == 'admin123':  
        return redirect(url_for('admin_panel'))
    return 'Invalid password'

@app.route('/admin/panel', methods=['GET', 'POST'])
def admin_panel():
    # Fetch all requests
    conn = sqlite3.connect('approval.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM requests')
    requests = cursor.fetchall()
    conn.close()
    return render_template_string(admin_template, requests=requests)

@app.route('/admin/approve/<int:request_id>', methods=['POST'])
def admin_approve(request_id):
    status = request.form['status']
    # Update status in database
    conn = sqlite3.connect('approval.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE requests SET status = ? WHERE id = ?', (status, request_id))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_panel'))

@app.route('/visit', methods=['GET'])
def visit():
    # Approved users ki list fetch karein
    conn = sqlite3.connect('approval.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM requests WHERE status = "approved"')
    approved_users = cursor.fetchall()
    conn.close()

    # Approved users ko specific URL par redirect karein
    name = request.args.get('name')
    for user in approved_users:
        if user[1] == name:
            return render_template_string(visit_template)
    return 'Access denied'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
