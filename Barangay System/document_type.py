from flask import flash, redirect, render_template
from app import app
from utils import db_cursor, login_required


# READ-ALL
@app.route('/read_all_doctype')
@login_required
def read_all_doctype():
    with db_cursor() as cursor:
        cursor.execute("SELECT * FROM tbldocumenttype ORDER BY Name")
        rows = cursor.fetchall()
    return render_template('readdoctypes.html', rows=rows)


# READ-ONE
@app.route('/read_one_doctype/<string:id>')
@login_required
def read_one_doctype(id):
    with db_cursor() as cursor:
        cursor.execute("SELECT * FROM tbldocumenttype WHERE DocTypeID=%s", (id,))
        row = cursor.fetchone()
    if row is None:
        flash('Document type %s was not found.' % id, 'danger')
        return redirect('/read_all_doctype')
    return render_template('viewdoctypes.html', row=row)
