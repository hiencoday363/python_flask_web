from flask import Flask, render_template, redirect, request, session, url_for
from sqlalchemy import create_engine
import os, math

app = Flask(__name__)

# create access token
app.secret_key = os.urandom(24)

#config database
server = 'databasehienco.cidw3wkwqevk.us-east-1.rds.amazonaws.com,1433' # to specify an alternate port
database = 'flask' 
username = 'hien363' 
password = 'hien0362363616'
driver = 'SQL Server'

engine = create_engine(f"mssql+pymssql://{username}:{password}@{server}/{database}?driver={driver}")

#connect 
conn = engine.connect()

print('connect')


# class error
class handle_error():
    type_username = ''
    type_email = ''
    type_pass = ''


@app.route('/index.html/<int:current_page>')
def hello_world(current_page):
    if 'user_id' in session and 'user_email' in session:
        limit = 4
        cursor1 = conn.execute("SELECT * FROM article")

        total_page = math.ceil(len(cursor1.fetchall()) / limit) + 1

        cursor2 = conn.execute("SELECT * FROM article ORDER BY ngaydang DESC OFFSET (? - 1)*?  ROWS FETCH FIRST ? ROWS ONLY;",
                       current_page, limit, limit)

        rows = cursor2.fetchall()

        data = [current_page, total_page, rows]

        cursor3 = conn.execute("SELECT * FROM login_dk WHERE email LIKE ?", session['user_email'])
        user_email = cursor3.fetchall()

        return render_template('home.html', data=data, account=user_email[0][1])
    else:
        return redirect('/')


@app.route('/detail/<int:id_page>')
def detail(id_page):
    if 'user_id' in session:
        cursor = conn.execute('SELECT * FROM article WHERE ID = ?', id_page)

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
        conn.execute('UPDATE article SET title = ?, content = ?, img = ?  WHERE ID = ?', title, message, link,
                       id_page)

        return redirect(f'/detail/{id_page}')
    else:
        return redirect('/')


@app.route('/delete/<int:id_post>')
def delete(id_post):
    if 'user_id' in session:
        if id_post != 1:
            conn.execute('DELETE FROM article WHERE ID = ?', id_post)
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
        conn.execute('INSERT INTO article(title,content,img) VALUES(?,?,?)', title, message, link)
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
        # b2: check request
        cursor = conn.execute("SELECT * FROM login_dk WHERE email LIKE ?", email)
        rows_email = cursor.fetchall()
        if len(rows_email) <= 0:
            handle_error.type_email = 'Email have not active, try again !'
            return render_template('login.html', str_error=handle_error.type_email, value_email=email,
                                   value_pass=password)
        else:
            cursor = conn.execute("SELECT * FROM login_dk WHERE mk LIKE ?", password)
            rows_pass = cursor.fetchall()
            if len(rows_pass) <= 0:
                handle_error.type_pass = 'Password incorrect, please check it !'
                return render_template('login.html', str_error=handle_error.type_pass, value_email=email,
                                       value_pass=password)
            else:
                session['user_id'] = rows_pass[0][0]
                session['user_email'] = email
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
            rows_user = conn.execute("SELECT * FROM login_dk WHERE username = ?", username)
            if len(rows_user.fetchall()) > 0:
                handle_error.type_username = 'Name is not available !'
                return render_template('signup.html', str_error=handle_error.type_username, value_name=username,
                                       value_email=email, value_pass=password)
            else:
                rows_email = conn.execute("SELECT * FROM login_dk WHERE email = ?", email)
                if len(rows_email.fetchall()) > 0:
                    handle_error.type_email = 'Email is not available !'
                    return render_template('signup.html', str_error=handle_error.type_email, value_name=username,
                                           value_email=email, value_pass=password)
                else:
                    new_user = conn.execute("INSERT INTO login_dk(username, email, mk) VALUES (?,?,?)", username, email,
                                   password)

                    row_user = conn.execute("SELECT * FROM login_dk WHERE email = ? AND mk = ?", email, password)
                    _user = row_user.fetchall()
                    if len(_user) > 0:
                        session['user_id'] = _user[0][0]
                        session['user_email'] = email
                        return redirect('/index.html/1')
                    else:
                        return render_template('signup.html', str_error='Some thing went wrong, please sign in later !')


if __name__ == '__main__':
    # app.run(debug=True,port=8000)
    pass
