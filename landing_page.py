from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def landing_page():
    return render_template('landing.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle login form submission
        print("Login form submitted")  # Replace with actual login logic
        return redirect(url_for('dashboard'))  # Redirect to dashboard after login
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Handle registration form submission
        print("Register form submitted")  # Replace with actual registration logic
        return redirect(url_for('login'))  # Redirect to login after registration
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return "Welcome to your dashboard!"  # Replace with actual dashboard page

if __name__ == '__main__':
    app.run(debug=True)