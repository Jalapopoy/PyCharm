from flask import flash, redirect, render_template, request, session
from app import app
from utils import db_cursor, login_required


# LOG-IN PAGE
@app.route('/')
def login_user_view():
    return render_template('index.html')


# LOG-IN USER
@app.route('/log_in_user', methods=['POST'])
def log_in_user():
    strUser = request.form['Username'].strip()
    strPass = request.form['Password']

    with db_cursor() as cursor:
        cursor.execute("SELECT * FROM tbluser WHERE Username=%s AND Password=%s "
                       "AND LOWER(Status)='active'", (strUser, strPass))
        row = cursor.fetchone()

    if row is None:
        flash('Invalid username or password', 'danger')
        return redirect('/')

    # Only resident accounts (linked to a resident record) use this client.
    if not row['ResidentID']:
        flash('This account is not linked to a resident. Staff use the web application.', 'danger')
        return redirect('/')

    session.clear()
    session['user_id'] = row['UserID']
    session['username'] = row['Username']
    session['resident_id'] = row['ResidentID']
    return redirect('/home_page')


# HOME PAGE
@app.route('/home_page')
@login_required
def home_page():
    with db_cursor() as cursor:
        cursor.execute("SELECT FirstName, LastName FROM tblresident WHERE ResidentID=%s",
                       (session['resident_id'],))
        person = cursor.fetchone()
        cursor.execute("SELECT COUNT(*) AS n FROM tblrequest WHERE ResidentID=%s AND Status='Pending'",
                       (session['resident_id'],))
        pending = cursor.fetchone()['n']
    name = (person['FirstName'] + ' ' + person['LastName']) if person else session['username']
    return render_template('home.html', name=name, pending=pending)


# LOG-OUT
@app.route('/log_out')
def log_out():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect('/')
