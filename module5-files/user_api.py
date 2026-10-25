import pymysql
from app import app
from db import mysql
from flask import jsonify
from flask import flash, request

# CREATE USER API
@app.route('/create-user', methods=['POST'])
def add_user():
    conn = None
    cursor = None
    try:
        # GET JSON DATA
        _json = request.json
        _User_ID = _json['User_ID']
        _Last_Name = _json['Last_Name']
        _First_Name = _json['First_Name']
        _Middle_Name = _json['Middle_Name']
        _Home_Address = _json['Home_Address']
        _Email_Address = _json['Email_Address']
        _Mobile_Number = _json['Mobile_Number']
        _User_Type_ID = _json['User_Type_ID']
        _Status = _json['Status']
        _Password = _json['Password']

        # CHECK IF EMPTY
        if (_User_ID and _Last_Name and _First_Name and _Middle_Name and _Home_Address
                and _Email_Address and _Mobile_Number and _User_Type_ID and _Status and _Password
                and request.method == 'POST'):

            # SAVE RECORD
            sql = "INSERT INTO tbl_user_info(User_ID, Last_Name, First_Name, Middle_Name, Home_Address, Email_Address, Mobile_Number, User_Type_ID, Status, Password) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            data = (_User_ID, _Last_Name, _First_Name, _Middle_Name, _Home_Address, _Email_Address, _Mobile_Number,
                    _User_Type_ID, _Status, _Password)

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()

            resp = jsonify('Record added successfully!')
            resp.status_code = 200
            return resp
        else:
            return not_found()

    except Exception as e:
        print(e)

    finally:
        cursor.close()
        conn.close()


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp

#DELETE USER
@app.route('/delete-user/<id>', methods=['DELETE'])
def delete_user(id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tbl_user_info WHERE User_ID=%s", (id,))
        conn.commit()
        resp = jsonify('Record deleted successfully!')
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


# UPDATE USER
@app.route('/update-user', methods=['PUT'])
def update_user():
    conn = None
    cursor = None
    try:
        _json = request.json
        _User_ID = _json['User_ID']
        _Last_Name = _json['Last_Name']
        _First_Name = _json['First_Name']
        _Middle_Name = _json['Middle_Name']
        _Home_Address = _json['Home_Address']
        _Email_Address = _json['Email_Address']
        _Mobile_Number = _json['Mobile_Number']
        _User_Type_ID = _json['User_Type_ID']
        _Status = _json['Status']

        if (_User_ID and _Last_Name and _First_Name and _Middle_Name and _Home_Address
                and _Email_Address and _Mobile_Number and _User_Type_ID and _Status and request.method == 'PUT'):

            # save edits
            sql = "UPDATE tbl_user_info SET Last_Name=%s, First_Name=%s, Middle_Name=%s, Home_Address=%s, Email_Address=%s, Mobile_Number=%s, User_Type_ID=%s, Status=%s WHERE User_ID=%s"
            data = (_Last_Name, _First_Name, _Middle_Name, _Home_Address, _Email_Address, _Mobile_Number, _User_Type_ID,
                    _Status, _User_ID)

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()

            resp = jsonify('Record updated successfully!')
            resp.status_code = 200
            return resp

        else:
            return not_found()

    except Exception as e:
        print(e)

    finally:
        cursor.close()
        conn.close()

#READ ONE USER
@app.route('/read-one-user/<id>')
def user(id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT User_ID, Last_Name, First_Name, "
                       "Middle_Name, Home_Address, "
                       "Email_Address, Mobile_Number, uinfo.User_Type_ID, User_Type_Name, Status, "
                       "Password "
                       "FROM tbl_user_info uinfo "
                       "JOIN tbl_user_type utype "
                       "ON uinfo.User_Type_ID = utype.User_Type_ID WHERE User_ID=%s", id)
        row = cursor.fetchone()
        resp = jsonify(row)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

#READ ALL USER
@app.route('/read-all-user')
def users():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT User_ID, Last_Name, First_Name, "
                       "Middle_Name, Home_Address, "
                       "Email_Address, Mobile_Number, uinfo.User_Type_ID, User_Type_Name, Status, "
                       "Password "
                       "FROM tbl_user_info uinfo "
                       "JOIN tbl_user_type utype "
                       "ON uinfo.User_Type_ID = utype.User_Type_ID")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    app.run(debug=True, port=8080)