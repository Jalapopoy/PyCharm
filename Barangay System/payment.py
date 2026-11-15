from flask import flash, redirect, render_template, session
from app import app
from utils import db_cursor, login_required

# Payments belong to requests, so we find the resident's payments through tblrequest.
PAYMENT_QUERY = ("SELECT p.*, r.Purpose, d.Name AS DocName "
                 "FROM tblpayment p "
                 "JOIN tblrequest r ON p.RequestID = r.RequestID "
                 "LEFT JOIN tbldocumenttype d ON r.DocTypeID = d.DocTypeID "
                 "WHERE r.ResidentID=%s")


# READ-ALL (own payments)
@app.route('/read_all_payment')
@login_required
def read_all_payment():
    with db_cursor() as cursor:
        cursor.execute(PAYMENT_QUERY + " ORDER BY p.PaymentDate DESC", (session['resident_id'],))
        rows = cursor.fetchall()
    return render_template('readpayments.html', rows=rows)


# READ-ONE
@app.route('/read_one_payment/<string:id>')
@login_required
def read_one_payment(id):
    with db_cursor() as cursor:
        cursor.execute(PAYMENT_QUERY + " AND p.PaymentID=%s", (session['resident_id'], id))
        row = cursor.fetchone()
    if row is None:
        flash('Payment %s was not found.' % id, 'danger')
        return redirect('/read_all_payment')
    return render_template('viewpayments.html', row=row)
