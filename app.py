from flask import Flask, render_template, request, redirect, url_for, session, flash
import csv
import os

app = Flask(__name__)
app.secret_key = "secret key"  # 设置secret key以启用flash消息

######################
# 用.CSV文件代替database
######################

# 检查当前目录下是否存在 user_data.csv 文件
filename = 'user_data.csv'
if not os.path.isfile(filename):
    # 如果不存在则创建一个空的CSV文件
    with open(filename, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['username', 'password', 'email'])


# 定义函数，从csv文件中获取所有用户信息并以列表的形式返回
def get_users():
    user_list = []
    with open("user_data.csv", "r", newline="") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            user_list.append(row)
    return user_list


# 定义函数，将所有用户信息写入csv文件
def save_users(users):
    with open("user_data.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        for user in users:
            writer.writerow(user)


@app.route('/')
def index():
    # 如果已登录，则跳转到panel页面
    if 'username' in session:
        return redirect(url_for('panel'))
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = get_users()
        # 检查用户是否存在以及密码是否正确
        for user in users:
            if user[0] == username and user[1] == password:
                session['username'] = username
                return redirect(url_for('panel'))
        # 如果用户不存在或密码错误，则显示错误消息
        flash('用户名或密码错误')
        return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password1 = request.form['password1']
        password2 = request.form['password2']
        email = request.form['email']
        users = get_users()
        # 检查用户名是否已被注册
        for user in users:
            if user[0] == username:
                flash('该用户名已被注册')
                return redirect(url_for('register'))
            if user[2] == email:
                flash('该email已被注册')
                return redirect(url_for('register'))
        # 检查两次输入的密码是否相同
        if password1 != password2:
            flash('两次输入的密码不一致')
            return redirect(url_for('register'))
        if username == '' or password1 == '' or email == '':
            flash('注册资料不能为空')
            return redirect(url_for('register'))
        # 将新用户信息添加到用户列表
        users.append([username, password1, email])
        # 将用户列表保存到csv文件
        save_users(users)
        # 注册成功，显示成功消息
        flash('注册成功，请登录')
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/panel')
def panel():
    # 如果未登录，则跳转到登录页面
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('panel.html', username=session['username'])


@app.route('/logout')
def logout():
    # 从会话中删除用户名并返回主页
    session.pop('username', None)
    flash('您已成功退出')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
