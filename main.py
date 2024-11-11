from flask import Flask, request, render_template_string, jsonify, redirect, url_for
import uuid

app = Flask(__name__)

# In-memory storage for approvals (for demo purposes, can be moved to a database)
approvals = {}
admin_password = "THE FAIZU"  # Admin password

# User-side routes

# Route to send approval request from User
@app.route('/send_approval', methods=['POST'])
def send_approval():
    user_data = request.json
    unique_key = str(uuid.uuid4())  # Unique key generated for each user
    approvals[unique_key] = {'status': 'pending', 'lifetime_link': None}
    return jsonify({"message": "Approval request sent", "key": unique_key})

# Route to check approval status for the user
@app.route('/check_approval/<key>', methods=['GET'])
def check_approval(key):
    if key in approvals:
        approval = approvals[key]
        if approval['status'] == 'approved':
            return jsonify({"status": "approved", "lifetime_link": approval['lifetime_link']})
        return jsonify({"status": "pending"})
    return jsonify({"status": "not found"}), 404

# Main page for User (index.html)
@app.route('/')
def index():
    user_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Approval System</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                padding: 20px;
                text-align: center;
            }
            .button {
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                margin: 10px;
                border: none;
                cursor: pointer;
            }
            .button:hover {
                background-color: #45a049;
            }
            table {
                width: 50%;
                margin: 20px auto;
                border-collapse: collapse;
            }
            th, td {
                border: 1px solid #ddd;
                padding: 10px;
                text-align: center;
            }
        </style>
    </head>
    <body>
        <h1>Welcome to the Approval System</h1>
        <p>Please send your approval request:</p>
        <button class="button" onclick="sendApproval()">Send Approval Request</button>
        <br><br>
        <p id="status"></p>
        
        <hr>
        
        <h2>Admin Panel (For Admin Use)</h2>
        <table>
            <tr>
                <th>Key</th>
                <th>Status</th>
                <th>Action</th>
            </tr>
            {% for key, approval in approvals.items() %}
                <tr>
                    <td>{{ key }}</td>
                    <td>{{ approval.status }}</td>
                    <td>
                        {% if approval.status == 'pending' %}
                            <button class="button" onclick="approveRequest('{{ key }}')">Approve</button>
                            <button class="button" onclick="rejectRequest('{{ key }}')">Reject</button>
                        {% else %}
                            <span>Already Processed</span>
                        {% endif %}
                    </td>
                </tr>
            {% endfor %}
        </table>
        
        <script>
            function sendApproval() {
                fetch('/send_approval', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({}) // empty object as example
                })
                .then(response => response.json())
                .then(data => {
                    document.getElementById('status').textContent = "Approval Request Sent. Your Key: " + data.key;
                });
            }

            function approveRequest(key) {
                fetch('/admin/approve/' + key, {
                    method: 'POST'
                })
                .then(response => response.json())
                .then(data => {
                    alert(data.message);
                    location.reload();
                });
            }

            function rejectRequest(key) {
                fetch('/admin/reject/' + key, {
                    method: 'POST'
                })
                .then(response => response.json())
                .then(data => {
                    alert(data.message);
                    location.reload();
                });
            }
        </script>
    </body>
    </html>
    """
    return render_template_string(user_template, approvals=approvals)


# Admin-side routes

# Admin login page to input password
@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form['password']
        if password == admin_password:
            return redirect(url_for('admin_dashboard'))
        return "Incorrect Password! Please try again."

    return '''
    <html>
        <body>
            <h2>Admin Login</h2>
            <form method="POST">
                <label for="password">Password:</label>
                <input type="password" id="password" name="password">
                <button type="submit">Login</button>
            </form>
        </body>
    </html>
    '''

# Admin Dashboard to show all requests and approve/reject them
@app.route('/admin/dashboard', methods=['GET'])
def admin_dashboard():
    admin_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Admin Dashboard</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                padding: 20px;
                text-align: center;
            }
            table {
                width: 50%;
                margin: 20px auto;
                border-collapse: collapse;
            }
            th, td {
                border: 1px solid #ddd;
                padding: 10px;
                text-align: center;
            }
        </style>
    </head>
    <body>
        <h1>Admin Dashboard</h1>
        <table>
            <tr>
                <th>Key</th>
                <th>Status</th>
                <th>Action</th>
            </tr>
            {% for key, approval in approvals.items() %}
                <tr>
                    <td>{{ key }}</td>
                    <td>{{ approval.status }}</td>
                    <td>
                        {% if approval.status == 'pending' %}
                            <button class="button" onclick="approveRequest('{{ key }}')">Approve</button>
                            <button class="button" onclick="rejectRequest('{{ key }}')">Reject</button>
                        {% else %}
                            <span>Already Processed</span>
                        {% endif %}
                    </td>
                </tr>
            {% endfor %}
        </table>
        
        <script>
            function approveRequest(key) {
                fetch('/admin/approve/' + key, {
                    method: 'POST'
                })
                .then(response => response.json())
                .then(data => {
                    alert(data.message);
                    location.reload();
                });
            }

            function rejectRequest(key) {
                fetch('/admin/reject/' + key, {
                    method: 'POST'
                })
                .then(response => response.json())
                .then(data => {
                    alert(data.message);
                    location.reload();
                });
            }
        </script>
    </body>
    </html>
    """
    return render_template_string(admin_template, approvals=approvals)


# Admin action to approve a request
@app.route('/admin/approve/<key>', methods=['POST'])
def approve_request(key):
    if key in approvals and approvals[key]['status'] == 'pending':
        approvals[key]['status'] = 'approved'
        approvals[key]['lifetime_link'] = "https://herf-2-faizu-apk.onrender.com"  # Lifetime link for the user
        return jsonify({"message": "Approval granted"})
    return jsonify({"message": "Approval request not found or already handled"}), 404

# Admin action to reject a request
@app.route('/admin/reject/<key>', methods=['POST'])
def reject_request(key):
    if key in approvals and approvals[key]['status'] == 'pending':
        approvals[key]['status'] = 'rejected'
        return jsonify({"message": "Approval rejected"})
    return jsonify({"message": "Approval request not found or already handled"}), 404


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
