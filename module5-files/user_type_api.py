from importlib.metadata import requires
from logging import exception

import pymysql
from app import app
from db import mysql
from flask import jsonify
from flask import flash, request

from user_api import not_found

#CREATE
@app.route('/create-user-type', methods=['POST'])
def add_user_type():
    conn = None
    cursor = None
    try:
        #Get JSON Data
        _json = request.json
        _User_Type_ID = _json['User_Type_ID']
        _User_Type_Name = _json['User_Type_Name']
        _User_Type_Description = _json['User_Type_Description']

        #Check if empty
        if _User_Type_ID and _User_Type_Name and _User_Type_Description and request.method == 'POST':

            sql = "INSERT INTO tbl_user_type(User_Type_ID, User_Type_Name, User_Type_Description) VALUES (%s, %s, %s)"
            data = (_User_Type_ID, _User_Type_Name, _User_Type_Description)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('Record added successfully')
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
    message= {
        'status': 404,
        'message': 'Not Found' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

#READ ALL
@app.route('/read-all-user-type')
def user_types():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT User_Type_ID, User_Type_Name, User_Type_Description FROM tbl_user_type")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

#READ ONE
@app.route('/read-one-user-type/<id>')
def user_type(id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT User_Type_ID, User_Type_Name, User_Type_Description FROM tbl_user_type WHERE User_Type_ID=%s", id)
        row = cursor.fetchone()
        resp = jsonify(row)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

#UPDATE
@app.route('/update-user-type', methods=['PUT'])
def update_user_type():
    conn = None
    cursor = None
    try:
        _json = request.json
        _User_Type_ID = _json['User_Type_ID']
        _User_Type_Name = _json['User_Type_Name']
        _User_Type_Description = _json['User_Type_Description']

        if _User_Type_ID and _User_Type_Name and _User_Type_Description and request.method == 'PUT':

            sql = "UPDATE tbl_user_type SET User_Type_Name=%s, User_Type_Description=%s WHERE User_Type_ID=%s"
            data = (_User_Type_Name, _User_Type_Description, _User_Type_ID)

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

#DELETE
@app.route('/delete-user-type/<string:id>', methods=['DELETE'])
def delete_user_type(id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tbl_user_type WHERE User_Type_ID=%s", (id,))
        conn.commit()
        resp = jsonify('Record deleted successfully!')
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True, port=5050)