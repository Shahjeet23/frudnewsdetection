from flask import Flask, render_template, request, redirect, session
import csv
import os
import joblib

app = Flask(__name__)
app.secret_key = 'your-secret-key'

#fake_news_model_path = 'C:\Users\Pavilion\Desktop\prokect7\models\30fake_news_detection_model.h5'
#fake_image_model_path = 'models/fake_image_model.h5'
#fake_handwriting_model_path = 'models/fake_handwriting_model.h5'
#model_filename = '29fake_news_detection_model.h5'

# Load the trained model
#model = joblib.load(r'models\30fake_news_detection_model.h5')

# Fake News Detection Model
# Fake News Detection Model
#def fake_news_detection(news_content):
  # Add your code for fake_news_detection here

# Fake Image Detection Model
# Add your code for fake_image_detection here

# Fake Handwriting Detection Model
# Add your code for fake_handwriting_detection here

# File paths for storing user and admin data
users_data_file = 'C:\\Users\\Pavilion\\Desktop\\prokect7\\users.csv'
admins_data_file = 'C:\\Users\\Pavilion\\Desktop\\prokect7\\admins.csv'

# Helper function to load user data from CSV
def load_users():
    users_data = []
    with open(users_data_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            users_data.append(row)
    return users_data

# Helper function to load admin data from CSV
def load_admins():
    admins_data = []
    with open(admins_data_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            admins_data.append(row)
    return admins_data

# Helper function to save user data to CSV
def save_users(users_data):
    with open(users_data_file, mode='w', newline='') as file:
        fieldnames = ['username', 'password', 'history']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(users_data)

# Helper function to save admin data to CSV
def save_admins(admins_data):
    with open(admins_data_file, mode='w', newline='') as file:
        fieldnames = ['admin_username', 'admin_password', 'admin_history']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(admins_data)

# Home Page
@app.route('/')
def home():
    return render_template('home.html')

# Registration Page
@app.route('/register.html', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users_data = load_users()
        users_data.append({'username': username, 'password': password, 'history': []})
        save_users(users_data)
        return redirect('/login.html')
    return render_template('register.html')

# Login Page
@app.route('/login.html', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users_data = load_users()
        for user in users_data:
            if user['username'] == username and user['password'] == password:
                session['username'] = username
                return redirect('/index.html')
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

# Admin Registration Page
@app.route('/admin_register.html', methods=['GET', 'POST'])
def admin_register():
    if request.method == 'POST':
        admin_username = request.form['admin_username']
        admin_password = request.form['admin_password']
        admins_data = load_admins()
        admins_data.append({'admin_username': admin_username, 'admin_password': admin_password, 'admin_history': []})
        save_admins(admins_data)
        return redirect('/admin_login.html')
    return render_template('admin_register.html')

# Admin Login Page
@app.route('/admin_login.html', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        admin_username = request.form['admin_username']
        admin_password = request.form['admin_password']
        admins_data = load_admins()
        for admin in admins_data:
            if admin['admin_username'] == admin_username and admin['admin_password'] == admin_password:
                session['admin_username'] = admin_username
                return redirect('/admin.html')
        return render_template('admin_login.html', error='Invalid credentials')
    return render_template('admin_login.html')

# Logout
@app.route('/logout.html')
def logout():
    session.pop('username', None)
    session.pop('admin_username', None)
    return redirect('/')

# Index Page
@app.route('/index.html')
def index():
    if 'username' not in session:
        return redirect('/login.html')
    return render_template('index.html')
# Fake News Detection Page
@app.route('/fakenews.html', methods=['GET', 'POST'])
def fakenews():
    if 'username' not in session:
        return redirect('/login.html')

    if request.method == 'POST':
        news_content = request.form['news_content']
        result = fake_news_detection(news_content)
        return result

    return render_template('fakenews.html')

# Index Page

# Fake Image Detection Page
@app.route('/fakeimage.html', methods=['GET', 'POST'])
def fakeimage():
    if 'username' not in session:
        return redirect('/login.html')

    if request.method == 'POST':
        image_file = request.files['image_file']
        result = fake_image_detection(image_file)
        return render_template('fakeimage.html', image_file=image_file, result=result)

    return render_template('fakeimage.html')

# Fake Handwriting Detection Page
@app.route('/fakehandwriting.html', methods=['GET', 'POST'])
def fakehandwriting():
    if 'username' not in session:
        return redirect('/login.html')

    if request.method == 'POST':
        handwriting_sample = request.files['handwriting_sample']
        result = fake_handwriting_detection(handwriting_sample)
        return render_template('fakehandwriting.html', handwriting_sample=handwriting_sample, result=result)

    return render_template('fakehandwriting.html')


# Admin Page
# Admin Page
@app.route('/admin.html')
def admin():
    if 'admin_username' not in session:
        return redirect('/admin_login.html')
    admin_username = session.get('admin_username')
    if admin_username != 'admin':
        return redirect('/index.html')

    # Load users data and pass it to the template context
    users_data = load_users()
    users = {user['username']: user for user in users_data}

    # Load admin data and pass it to the template context
    admins_data = load_admins()
    admins = {admin['admin_username']: admin for admin in admins_data}

    return render_template('admin.html', users=users, admins=admins)



# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
