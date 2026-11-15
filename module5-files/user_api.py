import pymysql
from app import app
from db import mysql
from flask import jsonify
from flask import flash, request

# CREATE USER API
@app.route('/create-user', methods=['POST'])
def add_userJEM():
    connJEM = None
    cursorJEM = None
    try:
        # GET JSON DATA
        _jsonJEM = request.json
        _User_IDJEM = _jsonJEM['User_ID']
        _Last_NameJEM = _jsonJEM['Last_Name']
        _First_NameJEM = _jsonJEM['First_Name']
        _Middle_NameJEM = _jsonJEM['Middle_Name']
        _Home_AddressJEM = _jsonJEM['Home_Address']
        _Email_AddressJEM = _jsonJEM['Email_Address']
        _Mobile_NumberJEM = _jsonJEM['Mobile_Number']
        _User_Type_IDJEM = _jsonJEM['User_Type_ID']
        _StatusJEM = _jsonJEM['Status']
        _PasswordJEM = _jsonJEM['Password']

        # CHECK IF EMPTY
        if (_User_IDJEM and _Last_NameJEM and _First_NameJEM and _Middle_NameJEM and _Home_AddressJEM
                and _Email_AddressJEM and _Mobile_NumberJEM and _User_Type_IDJEM and _StatusJEM and _PasswordJEM
                and request.method == 'POST'):

            # SAVE RECORD
            sqlJEM = "INSERT INTO tbl_user_info(User_ID, Last_Name, First_Name, Middle_Name, Home_Address, Email_Address, Mobile_Number, User_Type_ID, Status, Password) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            dataJEM = (_User_IDJEM, _Last_NameJEM, _First_NameJEM, _Middle_NameJEM, _Home_AddressJEM, _Email_AddressJEM,
                       _Mobile_NumberJEM, _User_Type_IDJEM, _StatusJEM, _PasswordJEM)

            connJEM = mysql.connect()
            cursorJEM = connJEM.cursor()
            cursorJEM.execute(sqlJEM, dataJEM)
            connJEM.commit()

            respJEM = jsonify('Record added successfully!')
            respJEM.status_code = 200
            return respJEM
        else:
            return not_foundJEM()

    except Exception as eJEM:
        print(eJEM)

    finally:
        cursorJEM.close()
        connJEM.close()


@app.errorhandler(404)
def not_foundJEM(errorJEM=None):
    messageJEM = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    respJEM = jsonify(messageJEM)
    respJEM.status_code = 404
    return respJEM

#DELETE USER
@app.route('/delete-user/<idJEM>', methods=['DELETE'])
def delete_userJEM(idJEM):
    connJEM = None
    cursorJEM = None
    try:
        connJEM = mysql.connect()
        cursorJEM = connJEM.cursor()
        cursorJEM.execute("DELETE FROM tbl_user_info WHERE User_ID=%s", (idJEM,))
        connJEM.commit()
        respJEM = jsonify('Record deleted successfully!')
        respJEM.status_code = 200
        return respJEM
    except Exception as eJEM:
        print(eJEM)
    finally:
        cursorJEM.close()
        connJEM.close()


# UPDATE USER
@app.route('/update-user', methods=['PUT'])
def update_userJEM():
    connJEM = None
    cursorJEM = None
    try:
        _jsonJEM = request.json
        _User_IDJEM = _jsonJEM['User_ID']
        _Last_NameJEM = _jsonJEM['Last_Name']
        _First_NameJEM = _jsonJEM['First_Name']
        _Middle_NameJEM = _jsonJEM['Middle_Name']
        _Home_AddressJEM = _jsonJEM['Home_Address']
        _Email_AddressJEM = _jsonJEM['Email_Address']
        _Mobile_NumberJEM = _jsonJEM['Mobile_Number']
        _User_Type_IDJEM = _jsonJEM['User_Type_ID']
        _StatusJEM = _jsonJEM['Status']

        if (_User_IDJEM and _Last_NameJEM and _First_NameJEM and _Middle_NameJEM and _Home_AddressJEM
                and _Email_AddressJEM and _Mobile_NumberJEM and _User_Type_IDJEM and _StatusJEM and request.method == 'PUT'):

            # save edits
            sqlJEM = "UPDATE tbl_user_info SET Last_Name=%s, First_Name=%s, Middle_Name=%s, Home_Address=%s, Email_Address=%s, Mobile_Number=%s, User_Type_ID=%s, Status=%s WHERE User_ID=%s"
            dataJEM = (_Last_NameJEM, _First_NameJEM, _Middle_NameJEM, _Home_AddressJEM, _Email_AddressJEM,
                       _Mobile_NumberJEM, _User_Type_IDJEM, _StatusJEM, _User_IDJEM)

            connJEM = mysql.connect()
            cursorJEM = connJEM.cursor()
            cursorJEM.execute(sqlJEM, dataJEM)
            connJEM.commit()

            respJEM = jsonify('Record updated successfully!')
            respJEM.status_code = 200
            return respJEM

        else:
            return not_foundJEM()

    except Exception as eJEM:
        print(eJEM)

    finally:
        cursorJEM.close()
        connJEM.close()

#READ ONE USER
@app.route('/read-one-user/<idJEM>')
def userJEM(idJEM):
    connJEM = None
    cursorJEM = None
    try:
        connJEM = mysql.connect()
        cursorJEM = connJEM.cursor(pymysql.cursors.DictCursor)
        cursorJEM.execute("SELECT User_ID, Last_Name, First_Name, "
                          "Middle_Name, Home_Address, "
                          "Email_Address, Mobile_Number, uinfo.User_Type_ID, User_Type_Name, Status, "
                          "Password "
                          "FROM tbl_user_info uinfo "
                          "JOIN tbl_user_type utype "
                          "ON uinfo.User_Type_ID = utype.User_Type_ID WHERE User_ID=%s", idJEM)
        rowJEM = cursorJEM.fetchone()
        respJEM = jsonify(rowJEM)
        respJEM.status_code = 200
        return respJEM
    except Exception as eJEM:
        print(eJEM)
    finally:
        cursorJEM.close()
        connJEM.close()

#READ ALL USER
@app.route('/read-all-user')
def usersJEM():
    connJEM = None
    cursorJEM = None
    try:
        connJEM = mysql.connect()
        cursorJEM = connJEM.cursor(pymysql.cursors.DictCursor)
        cursorJEM.execute("SELECT User_ID, Last_Name, First_Name, "
                          "Middle_Name, Home_Address, "
                          "Email_Address, Mobile_Number, uinfo.User_Type_ID, User_Type_Name, Status, "
                          "Password "
                          "FROM tbl_user_info uinfo "
                          "JOIN tbl_user_type utype "
                          "ON uinfo.User_Type_ID = utype.User_Type_ID")
        rowsJEM = cursorJEM.fetchall()
        respJEM = jsonify(rowsJEM)
        respJEM.status_code = 200
        return respJEM
    except Exception as eJEM:
        print(eJEM)
    finally:
        cursorJEM.close()
        connJEM.close()


if __name__ == "__main__":
    app.run(debug=True, port=8080)