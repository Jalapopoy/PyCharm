# JSON API for the Request table (test it in Postman).
# 1) POST /log_in_user with form fields Username and Password (Postman keeps the cookie)
# 2) call the /api/requests routes below
from flask import jsonify, request, session
from app import app
from utils import db_cursor, login_required, next_id, own_request, has_paid_payment


def message(text, code):
    resp = jsonify({'message': text})
    resp.status_code = code
    return resp


# READ-ALL
@app.route('/api/requests', methods=['GET'])
@login_required
def api_read_all_requests():
    with db_cursor() as cursor:
        cursor.execute("SELECT * FROM tblrequest WHERE ResidentID=%s ORDER BY DateRequested DESC",
                       (session['resident_id'],))
        rows = cursor.fetchall()
    return jsonify(rows)


# READ-ONE
@app.route('/api/requests/<string:id>', methods=['GET'])
@login_required
def api_read_one_request(id):
    with db_cursor() as cursor:
        row = own_request(cursor, id)
    if row is None:
        return message('Request not found.', 404)
    return jsonify(row)


# CREATE   body: {"DocTypeID": "...", "Purpose": "...", "Remarks": "..."}
@app.route('/api/requests', methods=['POST'])
@login_required
def api_create_request():
    data = request.get_json(silent=True) or {}
    doctype = data.get('DocTypeID')
    purpose = (data.get('Purpose') or '').strip()
    remarks = (data.get('Remarks') or '').strip()
    if not doctype or not purpose:
        return message('DocTypeID and Purpose are required.', 400)

    with db_cursor() as cursor:
        cursor.execute("SELECT 1 FROM tbldocumenttype WHERE DocTypeID=%s", (doctype,))
        if cursor.fetchone() is None:
            return message('DocTypeID does not exist.', 400)
        new_id = next_id(cursor, 'tblrequest', 'RequestID', 'REQ')
        cursor.execute("INSERT INTO tblrequest (RequestID, ResidentID, DocTypeID, Purpose, "
                       "DateRequested, Status, Remarks) VALUES (%s, %s, %s, %s, NOW(), 'Pending', %s)",
                       (new_id, session['resident_id'], doctype, purpose, remarks))
    resp = jsonify({'message': 'Record added successfully!', 'RequestID': new_id})
    resp.status_code = 201
    return resp


# UPDATE   body: {"DocTypeID": "...", "Purpose": "...", "Remarks": "..."}
@app.route('/api/requests/<string:id>', methods=['PUT'])
@login_required
def api_update_request(id):
    data = request.get_json(silent=True) or {}
    doctype = data.get('DocTypeID')
    purpose = (data.get('Purpose') or '').strip()
    remarks = (data.get('Remarks') or '').strip()
    if not doctype or not purpose:
        return message('DocTypeID and Purpose are required.', 400)

    with db_cursor() as cursor:
        row = own_request(cursor, id)
        if row is None:
            return message('Request not found.', 404)
        if row['Status'] != 'Pending':
            return message('Only pending requests can be edited.', 400)
        cursor.execute("SELECT 1 FROM tbldocumenttype WHERE DocTypeID=%s", (doctype,))
        if cursor.fetchone() is None:
            return message('DocTypeID does not exist.', 400)
        cursor.execute("UPDATE tblrequest SET DocTypeID=%s, Purpose=%s, Remarks=%s "
                       "WHERE RequestID=%s AND ResidentID=%s",
                       (doctype, purpose, remarks, id, session['resident_id']))
    return message('Record updated successfully!', 200)


# DELETE
@app.route('/api/requests/<string:id>', methods=['DELETE'])
@login_required
def api_delete_request(id):
    with db_cursor() as cursor:
        row = own_request(cursor, id)
        if row is None:
            return message('Request not found.', 404)
        if row['Status'] != 'Pending':
            return message('Only pending requests can be cancelled.', 400)
        if has_paid_payment(cursor, id):
            return message('This request already has a payment.', 400)
        cursor.execute("DELETE FROM tblpayment WHERE RequestID=%s", (id,))
        cursor.execute("DELETE FROM tblrequest WHERE RequestID=%s AND ResidentID=%s",
                       (id, session['resident_id']))
    return message('Record deleted successfully!', 200)
