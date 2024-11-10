from flask import Flask, request, render_template, redirect, url_for, jsonify

app = Flask(__name__)

# In-memory data to store approval status (you can use a database in real-world applications)
approvals = {}

# Admin Password
ADMIN_PASSWORD = "THE FAIZU"

# Route to show the login page for admin
@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form['password']
        if password == ADMIN_PASSWORD:
            return redirect(url_for('admin_panel'))
        else:
            return "Incorrect password! Access denied.", 403
    
    return render_template('admin_login.html')

# Route to show the admin panel if the password is correct
@app.route('/admin-panel')
def admin_panel():
    return render_template('admin.html', approvals=approvals)

# Route to update approval status (Accept/Reject)
@app.route('/admin/update_approval', methods=['POST'])
def update_approval():
    data = request.get_json()
    username = data['username']
    action = data['action']
    
    if username in approvals:
        approvals[username]['status'] = action  # Update the approval status to accepted or rejected
    
    if action == 'accepted':
        approvals[username]['status'] = 'approved'  # Set permanent approval status
        return redirect(url_for('welcome', username=username))
    
    return jsonify({"status": "success"})

# Route to show the welcome page after approval
@app.route('/welcome/<username>')
def welcome(username):
    return render_template('welcome.html', username=username)

# Route for user to submit approval request
@app.route('/submit-approval', methods=['GET', 'POST'])
def submit_approval():
    if request.method == 'POST':
        username = request.form['username']
        if username not in approvals:
            approvals[username] = {'status': 'pending'}
        return redirect(url_for('admin_panel'))
    return render_template('submit_approval.html')

if __name__ == '__main__':
    app.run(debug=True)