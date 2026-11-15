from flask import flash, redirect, render_template, request, session
from app import app
from utils import db_cursor, login_required, next_id, own_request, has_paid_payment


def get_doctypes(cursor):
    cursor.execute("SELECT DocTypeID, Name, Fee FROM tbldocumenttype ORDER BY Name")
    return cursor.fetchall()


# READ-ALL (own requests)
@app.route('/read_all_request')
@login_required
def read_all_request():
    with db_cursor() as cursor:
        cursor.execute("SELECT r.*, d.Name AS DocName FROM tblrequest r "
                       "LEFT JOIN tbldocumenttype d ON r.DocTypeID = d.DocTypeID "
                       "WHERE r.ResidentID=%s ORDER BY r.DateRequested DESC",
                       (session['resident_id'],))
        rows = cursor.fetchall()
    return render_template('readrequests.html', rows=rows)


# CREATE (form)
@app.route('/create_request_view')
@login_required
def create_request_view():
    with db_cursor() as cursor:
        doctypes = get_doctypes(cursor)
    return render_template('requestform.html', mode='create', row=None, doctypes=doctypes)


# CREATE (save)
@app.route('/create_request', methods=['POST'])
@login_required
def create_request():
    strDocType = request.form['DocTypeID']
    strPurpose = request.form['Purpose'].strip()
    strRemarks = request.form.get('Remarks', '').strip()

    if not strDocType or not strPurpose:
        flash('Please choose a document and enter the purpose.', 'danger')
        return redirect('/create_request_view')

    with db_cursor() as cursor:
        cursor.execute("SELECT 1 FROM tbldocumenttype WHERE DocTypeID=%s", (strDocType,))
        if cursor.fetchone() is None:
            flash('That document type does not exist.', 'danger')
            return redirect('/create_request_view')

        new_id = next_id(cursor, 'tblrequest', 'RequestID', 'REQ')
        cursor.execute("INSERT INTO tblrequest (RequestID, ResidentID, DocTypeID, Purpose, "
                       "DateRequested, Status, Remarks) VALUES (%s, %s, %s, %s, NOW(), 'Pending', %s)",
                       (new_id, session['resident_id'], strDocType, strPurpose, strRemarks))

    flash('Request %s was submitted.' % new_id, 'success')
    return redirect('/read_all_request')


# READ-ONE
@app.route('/read_one_request/<string:id>')
@login_required
def read_one_request(id):
    with db_cursor() as cursor:
        cursor.execute("SELECT r.*, d.Name AS DocName, d.Fee AS DocFee FROM tblrequest r "
                       "LEFT JOIN tbldocumenttype d ON r.DocTypeID = d.DocTypeID "
                       "WHERE r.RequestID=%s AND r.ResidentID=%s", (id, session['resident_id']))
        row = cursor.fetchone()
    if row is None:
        flash('Request %s was not found.' % id, 'danger')
        return redirect('/read_all_request')
    return render_template('viewrequests.html', row=row)


# UPDATE (form)
@app.route('/update_request_view/<string:id>')
@login_required
def update_request_view(id):
    with db_cursor() as cursor:
        row = own_request(cursor, id)
        doctypes = get_doctypes(cursor)
    if row is None:
        flash('Request %s was not found.' % id, 'danger')
        return redirect('/read_all_request')
    if row['Status'] != 'Pending':
        flash('Only pending requests can be edited.', 'danger')
        return redirect('/read_all_request')
    return render_template('requestform.html', mode='edit', row=row, doctypes=doctypes)


# UPDATE (save)
@app.route('/update_request', methods=['POST'])
@login_required
def update_request():
    strID = request.form['RequestID']
    strDocType = request.form['DocTypeID']
    strPurpose = request.form['Purpose'].strip()
    strRemarks = request.form.get('Remarks', '').strip()

    with db_cursor() as cursor:
        row = own_request(cursor, strID)
        if row is None:
            flash('Request %s was not found.' % strID, 'danger')
            return redirect('/read_all_request')
        if row['Status'] != 'Pending':
            flash('Only pending requests can be edited.', 'danger')
            return redirect('/read_all_request')

        cursor.execute("SELECT 1 FROM tbldocumenttype WHERE DocTypeID=%s", (strDocType,))
        if cursor.fetchone() is None or not strPurpose:
            flash('Please choose a valid document and enter the purpose.', 'danger')
            return redirect('/update_request_view/' + strID)

        cursor.execute("UPDATE tblrequest SET DocTypeID=%s, Purpose=%s, Remarks=%s "
                       "WHERE RequestID=%s AND ResidentID=%s",
                       (strDocType, strPurpose, strRemarks, strID, session['resident_id']))

    flash('Request %s was updated.' % strID, 'success')
    return redirect('/read_all_request')


# DELETE (confirmation page)
@app.route('/delete_request_view/<string:id>')
@login_required
def delete_request_view(id):
    with db_cursor() as cursor:
        cursor.execute("SELECT r.*, d.Name AS DocName FROM tblrequest r "
                       "LEFT JOIN tbldocumenttype d ON r.DocTypeID = d.DocTypeID "
                       "WHERE r.RequestID=%s AND r.ResidentID=%s", (id, session['resident_id']))
        row = cursor.fetchone()
    if row is None:
        flash('Request %s was not found.' % id, 'danger')
        return redirect('/read_all_request')
    if row['Status'] != 'Pending':
        flash('Only pending requests can be cancelled.', 'danger')
        return redirect('/read_all_request')
    return render_template('deleterequests.html', row=row)


# DELETE (confirmed)
@app.route('/delete_request', methods=['POST'])
@login_required
def delete_request():
    strID = request.form['RequestID']
    with db_cursor() as cursor:
        row = own_request(cursor, strID)
        if row is None:
            flash('Request %s was not found.' % strID, 'danger')
            return redirect('/read_all_request')
        if row['Status'] != 'Pending':
            flash('Only pending requests can be cancelled.', 'danger')
            return redirect('/read_all_request')
        if has_paid_payment(cursor, strID):
            flash('This request already has a payment, so it cannot be cancelled here.', 'danger')
            return redirect('/read_all_request')

        # no foreign keys, so remove the unpaid payment record ourselves
        cursor.execute("DELETE FROM tblpayment WHERE RequestID=%s", (strID,))
        cursor.execute("DELETE FROM tblrequest WHERE RequestID=%s AND ResidentID=%s",
                       (strID, session['resident_id']))

    flash('Request %s was cancelled.' % strID, 'success')
    return redirect('/read_all_request')
