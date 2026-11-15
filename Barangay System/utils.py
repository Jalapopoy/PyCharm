import pymysql
from contextlib import contextmanager
from functools import wraps
from flask import jsonify, redirect, request, session
from db_config import mysql


@contextmanager
def db_cursor():
    """Opens a connection, gives a dictionary cursor, commits, then always closes."""
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        yield cursor
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()


def login_required(f):
    """Blocks a page unless the resident is logged in."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'resident_id' not in session:
            if request.path.startswith('/api/'):
                return jsonify({'message': 'Please log in first.'}), 401
            return redirect('/')
        return f(*args, **kwargs)
    return wrapper


def next_id(cursor, table, column, prefix):
    """Makes the next free ID such as REQ-001 (table and column are fixed names from our code)."""
    cursor.execute("SELECT COUNT(*) AS n FROM " + table)
    number = cursor.fetchone()['n'] + 1
    while True:
        new_id = "%s-%03d" % (prefix, number)
        cursor.execute("SELECT 1 FROM " + table + " WHERE " + column + "=%s", (new_id,))
        if cursor.fetchone() is None:
            return new_id
        number += 1


def own_request(cursor, request_id):
    """Returns the request only if it belongs to the logged-in resident."""
    cursor.execute("SELECT * FROM tblrequest WHERE RequestID=%s AND ResidentID=%s",
                   (request_id, session['resident_id']))
    return cursor.fetchone()


def has_paid_payment(cursor, request_id):
    cursor.execute("SELECT 1 FROM tblpayment WHERE RequestID=%s AND Status='Paid'", (request_id,))
    return cursor.fetchone() is not None
