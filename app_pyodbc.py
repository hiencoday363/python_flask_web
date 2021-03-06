from flask import Flask, render_template, redirect, request, session, url_for
import pyodbc
import os, math

app = Flask(__name__)

# create access token
app.secret_key = os.urandom(24)
'''
conn = pyodbc.connect(
    'Driver={SQL Server};'
    'Server=databasehienco.cidw3wkwqevk.us-east-1.rds.amazonaws.com,1433;'
    'uid=hien363;'
    'pwd=hien0362363616;'
    'Database=flask;'
    'Trusted_Connection=no;'
)
print('connect')
'''
conn = pyodbc.connect(
        'Driver={SQL Server};'
        'Server=DESKTOP-G2RKN51\\SQLEXPRESS;'
        'Username=sa;'
        'Password=hien123;'
        'Database=flask;'
        'Trusted_Connection=true;'
    )
print('connect')

# class error
class handle_error():
    type_username = ''
    type_email = ''
    type_pass = ''


@app.route('/index.html/<int:current_page>')
def hello_world(current_page):
    if 'user_id' in session:
        limit = 4
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM article")

        total_page = math.ceil(len(cursor.fetchall()) / limit) + 1

        cursor.execute("SELECT * FROM article ORDER BY ngaydang DESC OFFSET (? - 1)*?  ROWS FETCH FIRST ? ROWS ONLY;",
                       current_page, limit, limit)
        rows = cursor.fetchall()

        data = [current_page, total_page, rows]
        # cursor.execute("SELECT * FROM ")

        return render_template('home.html', data=data)
        # return f'{data[2]}'
    else:
        return redirect('/')


@app.route('/detail/<int:id_page>')
def detail(id_page):
    if 'user_id' in session:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM article WHERE ID = ?', id_page)
        row = cursor.fetchone()
        return render_template('detail.html', data=row)
    else:
        return redirect('/')


@app.route('/detail/edit/<int:id_page>', methods=['GET', 'POST'])
def edit(id_page):
    title = request.form.get('title')
    link = request.form.get('link')
    message = request.form.get('message')

    if 'user_id' in session:
        cursor = conn.cursor()
        cursor.execute('UPDATE article SET title = ?, content = ?, img = ?  WHERE ID = ?', title, message, link,
                       id_page)
        cursor.commit()

        row = [id_page, title, message, '', link]

        return redirect(f'/detail/{id_page}')
        # return render_template('detail.html', data=row)
    else:
        return redirect('/')


@app.route('/delete/<int:id_post>')
def delete(id_post):
    if 'user_id' in session:
        if id_post != 1:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM article WHERE ID = ?', id_post)
            cursor.commit()
        return redirect('/index.html/1')
    else:
        return redirect('/')


@app.route('/add_post', methods=['POST'])
def add_post():
    title = request.form.get('title')
    link = request.form.get('link')
    message = request.form.get('message')

    if title == '' or link == '' or message == '':
        return redirect('/index.html/1')
    else:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO article(title,content,img) VALUES(?,?,?)', title, message, link)
        cursor.commit()
        return redirect('/index.html/1')

# authenticate

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')


@app.route('/')
def login():
    if 'user_id' in session:
        return redirect('/index.html/1')
    else:
        return render_template('login.html')


@app.route('/login_validate', methods=['POST'])
def login_validate():
    # b1: get request
    email = request.form.get('email')
    password = request.form.get('password')

    if email == '' or password == '':
        return render_template('login.html', str_error='Please, fill in field')
    else:
        cursor = conn.cursor()
        # b2: check request
        cursor.execute("SELECT * FROM login_dk WHERE email LIKE ?", email)
        rows_email = cursor.fetchall()
        if len(rows_email) <= 0:
            handle_error.type_email = 'Email have not active, try again !'
            return render_template('login.html', str_error=handle_error.type_email, value_email=email,
                                   value_pass=password)
        else:
            cursor.execute("SELECT * FROM login_dk WHERE mk LIKE ?", password)
            rows_pass = cursor.fetchall()
            if len(rows_pass) <= 0:
                handle_error.type_pass = 'Password incorrect, please check it !'
                return render_template('login.html', str_error=handle_error.type_pass, value_email=email,
                                       value_pass=password)
            else:
                session['user_id'] = rows_pass[0][0]
                return redirect('/index.html/1')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/signup_validate', methods=['POST'])
def signup_validate():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    if len(username) < 5:
        handle_error.type_username = 'Field username min length = 5'
        return render_template('signup.html', str_error=handle_error.type_username, value_name=username,
                               value_email=email, value_pass=password)
    else:
        if len(password) < 5:
            handle_error.type_pass = 'Field password min length = 5'
            return render_template('signup.html', str_error=handle_error.type_pass, value_name=username,
                                   value_email=email, value_pass=password)
        else:
            cursor = conn.cursor()
            rows_user = cursor.execute("SELECT * FROM login_dk WHERE username = ?", username)
            if len(list(rows_user)) > 0:
                handle_error.type_username = 'Name is not available !'
                return render_template('signup.html', str_error=handle_error.type_username, value_name=username,
                                       value_email=email, value_pass=password)
            else:
                rows_email = cursor.execute("SELECT * FROM login_dk WHERE email = ?", email)
                if len(list(rows_email)) > 0:
                    handle_error.type_email = 'Email is not available !'
                    return render_template('signup.html', str_error=handle_error.type_email, value_name=username,
                                           value_email=email, value_pass=password)
                else:
                    cursor.execute("INSERT INTO login_dk(username, email, mk) VALUES (?,?,?)", username, email,
                                   password)
                    cursor.commit()
                    cursor.execute("SELECT * FROM login_dk WHERE email = ? AND mk = ?", email, password)
                    _user = cursor.fetchall()
                    if len(_user) > 0:
                        session['user_id'] = _user[0][0]
                        return redirect('/index.html/1')
                    else:
                        return render_template('signup.html', str_error='Some thing went wrong, please sign in later !')


if __name__ == '__main__':
    # app.run(debug=True,port=8000)
    pass
