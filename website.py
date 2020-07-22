try:
    from flask import Flask, render_template, request, redirect, url_for, session
    from cryptography.fernet import Fernet
    import sqlite3
    import re
    import os

    print("All modules loaded....")
except:
    print("Some Modules are missing....")

app = Flask(__name__)
app.secret_key = os.urandom(24)

'''
This method is called on hitting the utl - http://127.0.0.1:5000/flask-intro/ when the
application is loaded for the very first time to display the login page
'''


@app.route('/flask-intro/', methods=['GET', 'POST'])
def login():
    conn = sqlite3.connect('application.db')
    msg = ''

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:

        username = request.form['username']
        password = request.form['password']

        c = conn.cursor()

        c.execute('SELECT * FROM SECURITY')
        for row in c.fetchone():
            str_key = str(row, 'utf-8')
            cipher_suite = Fernet(str.encode(str_key))

            c.execute('SELECT * FROM account WHERE username = ?', (username,))
            for user in c.fetchall():

                decrypted_password = cipher_suite.decrypt(user[1])
                conn.commit()
                conn.close()
                if password == str(decrypted_password, 'utf-8'):
                    session['loggedin'] = True
                    session['username'] = username
            return redirect(url_for('home'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('login.html', msg=msg)


'''
This method is called when the user wants to register and get his user id and password to login to the
application.
'''


@app.route('/flask-intro/register', methods=['GET', 'POST'])
def register():
    conn = sqlite3.connect('application.db')
    msg = ''
    if request.method == 'POST' and 'first_name' in request.form and 'last_name' in request.form and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        c = conn.cursor()

        c.execute('SELECT * FROM account WHERE username = ?', (username,))

        account = c.fetchone()

        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not first_name or not last_name or not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            c.execute('SELECT * FROM SECURITY')

            for row in c.fetchone():
                str_key = str(row, 'utf-8')
                cipher_suite = Fernet(str.encode(str_key))
                encrypted_password = cipher_suite.encrypt(str.encode(password))

                c.execute('INSERT INTO account VALUES(?,?,?,?,?)',
                          (username, encrypted_password, first_name, last_name, email))
            conn.commit()
            conn.close()
        msg = 'You have successfully registered!'
    elif request.method == 'POST':

        msg = 'Please fill out the form!'
    return render_template('register.html', msg=msg)


'''
This method is called when the user clicks on logout button
'''


@app.route('/flask-intro/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('login'))


'''
This method is called when a logged in user clicks the home button on the top nav bar
'''


@app.route('/flask-intro/home')
def home():
    if 'loggedin' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))


'''
This method is called when a logged in user clicks on add candidate button on the top nav bar
'''


@app.route('/flask-intro/add_candidate')
def add_candidate():
    if 'loggedin' in session:
        return render_template('candidate.html')
    return redirect(url_for('login'))


'''
This method is called when a logged in user clicks on search candidate button on the top nav bar
'''


@app.route('/flask-intro/search_candidate')
def search_candidate():
    if 'loggedin' in session:
        return render_template('search-candidate.html')
    return redirect(url_for('login'))


'''
This method is called when a logged in user saves the candidate details
'''


@app.route('/flask-intro/save_candidate', methods=['POST', 'GET'])
def save_candidate():
    msg = ''
    if 'loggedin' in session:
        conn = sqlite3.connect('application.db')

        if request.method == 'POST':
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            phone_number = request.form['phone_number']
            current_location = request.form['current_location']
            work_authorization = request.form['work_authorization']
            resume_upload = request.files['resume_upload']
            docs_upload = request.files['docs_upload']
            initial_status = 'INITIAL SCREENING'

            c = conn.cursor()

            c.execute('SELECT * FROM SECURITY')

            for row in c.fetchone():
                str_key = str(row, 'utf-8')
                cipher_suite = Fernet(str.encode(str_key))
                encrypted_docs = cipher_suite.encrypt(docs_upload.read())

                c.execute('INSERT INTO candidate VALUES(?,?,?,?,?,?,?,?,?)',
                          (first_name, last_name, email, phone_number, current_location, work_authorization,
                           resume_upload.read(),
                           encrypted_docs, initial_status))
            conn.commit()
            conn.close()
            msg = 'You have successfully added candidate!'
        elif request.method == 'POST':
            msg = 'Please fill out the form!'
        return render_template('candidate.html', msg=msg)
    return redirect(url_for('login'))


'''
This method is called when a logged in user searches for a particular candidate using the email id
'''


@app.route('/flask-intro/search_result', methods=['POST', 'GET'])
def search_result():
    msg = ''
    if 'loggedin' in session:
        conn = sqlite3.connect('application.db')

        if request.method == 'POST' and 'email' in request.form:
            email = request.form['email']
            c = conn.cursor()

            c.execute('SELECT * FROM CANDIDATE WHERE email = ?', (email,))

            candidate_list = c.fetchall()
            conn.commit()
            conn.close()

            if candidate_list:

                return render_template('search-result.html', msg=msg, candidate_list=candidate_list)
            else:
                msg = 'No candidate found matching the search criteria'
                return render_template('search-candidate.html', msg=msg)
        elif request.method == 'POST':
            msg = 'Please enter the search criteria!'
            return render_template('search-candidate.html', msg=msg)
    return redirect(url_for('login'))


'''
This method is called when a logged in user deletes a candidate's record
'''


@app.route('/flask-intro/delete', methods=['POST', 'GET'])
def delete():
    msg = ''
    if 'loggedin' in session:
        conn = sqlite3.connect('application.db')

        if request.method == 'POST' and 'email' in request.form:
            email = request.form['email']
            c = conn.cursor()

            c.execute('DELETE FROM CANDIDATE WHERE email = ?', (email,))

            conn.commit()
            conn.close()

            msg = 'Candidate Deleted Successfully'
        return render_template('candidate.html', msg=msg)
    return redirect(url_for('login'))


'''
This method is called when a logged in user clicks on view candidate button on the top nav bar
'''


@app.route('/flask-intro/view_candidate')
def view_candidate():
    if 'loggedin' in session:
        return render_template('search-for-view-candidate.html')
    return redirect(url_for('login'))


'''
This method is called when a logged in user clicks on update candidate button on the top nav bar
'''


@app.route('/flask-intro/search_update_result', methods=['POST', 'GET'])
def search_update_result():
    msg = ''
    if 'loggedin' in session:
        conn = sqlite3.connect('application.db')

        if request.method == 'POST' and 'email' in request.form:
            email = request.form['email']
            c = conn.cursor()

            c.execute('SELECT * FROM CANDIDATE WHERE email = ?', (email,))

            candidate_list = c.fetchall()
            conn.commit()
            conn.close()

            if candidate_list:

                return render_template('search-update-result.html', msg=msg, candidate_list=candidate_list)
            else:
                msg = 'No candidate found matching the search criteria'
                return render_template('search-candidate.html', msg=msg)
        elif request.method == 'POST':
            msg = 'Please enter the search criteria!'
            return render_template('search-candidate.html', msg=msg)
    return redirect(url_for('login'))


'''
This method is called when a logged in user edits the candidate's information
'''


@app.route('/flask-intro/edit', methods=['POST', 'GET'])
def edit():
    msg = ''
    if 'loggedin' in session:
        conn = sqlite3.connect('application.db')

        if request.method == 'POST':
            first_name = request.form['new_first_name']
            last_name = request.form['new_last_name']
            email = request.form['new_email']
            old_email = request.form['old_email']
            phone_number = request.form['new_phone_number']
            current_location = request.form['new_current_location']
            work_authorization = request.form['new_work_authorization']
            status = request.form['new_status']

            c = conn.cursor()

            sql = 'UPDATE candidate SET firstname = ?, lastname = ?, email = ?, phonenumber = ?, currentlocation = ?, ' \
                  'workauthorization = ?, resume = ?, documents = ?, status = ? WHERE email = ? '

            data = (
                first_name, last_name, email, phone_number, current_location, work_authorization, '', '', status,
                old_email)

            c.execute(sql, data)

            c.execute('SELECT * FROM CANDIDATE WHERE email = ?', (email,))

            candidate_list = c.fetchall()

            conn.commit()
            conn.close()
            msg = 'You have successfully updated candidate!'

        return render_template('search-update-result.html', msg=msg, candidate_list=candidate_list)
    return redirect(url_for('login'))


'''
This method is called when a logged in user views the candidate's details
'''


@app.route('/flask-intro/view', methods=['POST', 'GET'])
def view():
    msg = ''
    if 'loggedin' in session:
        conn = sqlite3.connect('application.db')

        if request.method == 'POST' and 'email' in request.form:
            email = request.form['email']
            c = conn.cursor()

            c.execute('SELECT * FROM CANDIDATE WHERE email = ?', (email,))

            candidate_list = c.fetchall()
            conn.commit()
            conn.close()

            if candidate_list:

                return render_template('view-candidate.html', msg=msg, candidate_list=candidate_list)
            else:
                msg = 'No candidate found matching the search criteria'
                return render_template('search-for-view-candidate.html', msg=msg)
        elif request.method == 'POST':
            msg = 'Please enter the search criteria!'
            return render_template('search-for-view-candidate.html', msg=msg)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
