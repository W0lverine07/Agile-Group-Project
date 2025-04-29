from project import app
from flask import render_template,request

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/account')
def account():
    return render_template('account.html')
@app.route('/faqs')
def faqs():
    return render_template('faqs.html')
@app.route('/health_data',methods=['GET','POST'])
def health_data():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print(username,password)
    return render_template('health_data.html')

@app.route('/history')
def history():
    return render_template('history.html')
@app.route('/share_page')
def share_page():
    return render_template('share_page.html')

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/visualize')
def visualize():
    return render_template('visualize.html')

@app.route('/login',methods=['GET','POST'])
def login():
    return render_template('login.html')