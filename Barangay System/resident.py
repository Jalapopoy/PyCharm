from flask import flash, redirect, render_template, session
from app import app
from utils import db_cursor, login_required

# A resident may only see the members of their own household.
SAME_HOUSEHOLD = "HouseholdID = (SELECT HouseholdID FROM tblresident WHERE ResidentID=%s)"


# READ-ALL (household members)
@app.route('/read_all_resident')
@login_required
def read_all_resident():
    with db_cursor() as cursor:
        cursor.execute("SELECT * FROM tblresident WHERE " + SAME_HOUSEHOLD +
                       " ORDER BY LastName, FirstName", (session['resident_id'],))
        rows = cursor.fetchall()
    return render_template('readresidents.html', rows=rows)


# READ-ONE
@app.route('/read_one_resident/<string:id>')
@login_required
def read_one_resident(id):
    with db_cursor() as cursor:
        cursor.execute("SELECT * FROM tblresident WHERE ResidentID=%s AND " + SAME_HOUSEHOLD,
                       (id, session['resident_id']))
        row = cursor.fetchone()
    if row is None:
        flash('Resident %s was not found in your household.' % id, 'danger')
        return redirect('/read_all_resident')
    return render_template('viewresidents.html', row=row)
