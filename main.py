from flask import Flask, render_template_string, request, redirect, url_for, jsonify
import json

app = Flask(__name__)

# Sample data structure to store approval requests
approval_data = {
    "pending_requests": [],
    "approved_requests": [],
    "rejected_requests": []
}

# Load the approval data from JSON (for persistence)
def load_data():
    try:
        with open("approvals.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return approval_data

# Save the approval data to JSON
def save_data(data):
    with open("approvals.json", "w") as f:
        json.dump(data, f, indent=4)

# HTML for user-side and admin panel combined into one file
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        data = load_data()
        # Add pending request to approval data
        data['pending_requests'].append({'name': name})
        save_data(data)
        return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to Faizu APK</title>
    <style>
        body {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
            background-color: black;
            font-family: Arial, sans-serif;
            color: white;
        }
        img {
            max-width: 80%;
            height: auto;
        }
        h1 {
            margin: 20px 0;
            font-size: 24px;
        }
        .visit-button {
            padding: 10px 20px;
            font-size: 16px;
            color: white;
            background-color: #ff5733;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            text-decoration: none;
            transition: all 0.3s ease;
            box-shadow: 0 0 5px rgba(255, 87, 51, 0.6), 0 0 10px rgba(255, 87, 51, 0.6);
        }
        .visit-button:hover {
            background-color: #c0392b;
            box-shadow: 0 0 10px rgba(255, 87, 51, 1), 0 0 20px rgba(255, 87, 51, 1);
        }
        .admin-btn {
            margin-top: 20px;
            padding: 10px 20px;
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        .admin-btn:hover {
            background-color: #2980b9;
        }
    </style>
</head>
<body>
    <img src="https://raw.githubusercontent.com/FaiziXd/Lun-dhek-le-aja/refs/heads/main/220f94e79d9b080717913e25a523a917.jpg" alt="Faizu APK Image">
    <h1>Welcome Dear, Click and enjoy Faizu APK</h1>
    <a href="https://www.facebook.com/The.drugs.ft.chadwick.67" class="visit-button">Visit</a>
    <h3>Your approval is pending. Please wait.</h3>
    <!-- Option to enter admin password -->
    <form action="/admin" method="get">
        <button class="admin-btn" type="submit">Enter to Admin Panel</button>
    </form>
</body>
</html>
""")

    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Enter Your Name</title>
</head>
<body>
    <h1>Enter Your Name</h1>
    <form method="POST">
        <input type="text" name="name" placeholder="Enter Name" required>
        <button type="submit">Submit</button>
    </form>
</body>
</html>
""")

# Admin login page (where admin enters the password)
@app.route('/admin', methods=['GET', 'POST'])
def admin_panel():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == 'THE FAIZU':
            data = load_data()
            return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Panel</title>
</head>
<body>
    <h1>Admin Panel</h1>
    <h2>Pending Requests</h2>
    <ul>
        {% for request in data['pending_requests'] %}
            <li>{{ request['name'] }} 
                <form action="/approve/{{ request['name'] }}" method="POST">
                    <button type="submit">Approve</button>
                </form>
                <form action="/reject/{{ request['name'] }}" method="POST">
                    <button type="submit">Reject</button>
                </form>
            </li>
        {% endfor %}
    </ul>
</body>
</html>
""", data=load_data())
        else:
            return "Incorrect password. Please try again."

    return render_template_string("""
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
        <label for="password">Password:</label>
        <input type="password" id="password" name="password" required>
        <button type="submit">Submit</button>
    </form>
</body>
</html>
""")

# Handle approval actions
@app.route('/approve/<name>', methods=['POST'])
def approve(name):
    data = load_data()
    for req in data['pending_requests']:
        if req['name'] == name:
            data['approved_requests'].append(req)
            data['pending_requests'].remove(req)
            save_data(data)
            return redirect('/admin')
    return "Request not found."

# Handle rejection actions
@app.route('/reject/<name>', methods=['POST'])
def reject(name):
    data = load_data()
    for req in data['pending_requests']:
        if req['name'] == name:
            data['rejected_requests'].append(req)
            data['pending_requests'].remove(req)
            save_data(data)
            return redirect('/admin')
    return "Request not found."

# Run the Flask app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
