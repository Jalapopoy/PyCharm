from csv import excel_tab

import pymysql
from app import app
from db_config import mysql
from flask import flash, render_template, request, redirect

#View Read-All Page
@app.route('/read_all_stud')
def read_all_stud():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM tbl_stud_info")
        rows = cursor.fetchall()
        return render_template('readstuds.html', rows=rows)
    except Exception as e:
        print(e)
        return str(e), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/create_stud_view')
def create_stud_view():
    return render_template('addstuds.html')

#POST METHOD to Save New Student Record
@app.route('/create_stud', methods=['POST'])
def create_stud():
    conn = None
    cursor = None
    try:
        strID = request.form['StudID']
        strLName = request.form['LastName']
        strFName = request.form['FirstName']
        strMName = request.form['MiddleName']
        strHomeAdd = request.form['Address']
        strEmailAdd = request.form['EmailAdd']
        strAge = request.form['Age']
        strBirthday = request.form['Birthday']
        strGender = request.form['Gender']
        strCourse = request.form['Course']

        if request.method == 'POST':
            sql = "INSERT INTO tbl_stud_info \
                (Student_ID, Last_Name, First_Name, Middle_Name, Home_Address, \
                 Email_Address,Age, Birthday, Gender, Course) \
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            data = (strID, strLName, strFName, strMName, strHomeAdd, strEmailAdd, strAge, strBirthday, strGender, strCourse)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            flash('Record successfully saved in the database')
            return redirect('/read_all_stud')
        else:
            return 'Error while adding student'
    except Exception as e:
        print(e)
        return str(e), 500
    finally:
        cursor.close()
        conn.close()


#View Read-One Page
@app.route('/read_one_stud/<string:id>')
def read_one_stud(id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM tbl_stud_info WHERE student_id=%s", id)
        row = cursor.fetchone()
        if row:
            return render_template('viewstuds.html', row=row)
        else:
            return 'Error loading #{id}'.format(id=id)
    except Exception as e:
        print(e)
        return str(e), 500
    finally:
        cursor.close()
        conn.close()

#View Update Page
@app.route('/update_stud_view/<string:id>')
def update_stud_view(id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM tbl_stud_info WHERE Student_ID=%s", id)
        row = cursor.fetchone()
        if row:
            return render_template('editstuds.html', row=row)
        else:
            return 'Error loading #{id}.format(id=id)'
    except Exception as e:
        print(e)
        return str(e), 500
    finally:
        cursor.close()
        conn.close()

#POST Method to Save Changes in data
@app.route('/update_stud', methods=['POST'])
def update_stud():
    conn = None
    cursor = None
    try:
        # GET STUDENT INPUTS
        strID = request.form['StudID']
        strLName = request.form['LastName']
        strFName = request.form['FirstName']
        strMName = request.form['MiddleName']
        strHomeAdd = request.form['Address']
        strEmailAdd = request.form['EmailAdd']
        strAge = request.form['Age']
        strBirthday = request.form['Birthday']
        strGender = request.form['Gender']
        strCourse = request.form['Course']

        if request.method == 'POST':
            #SAVE CHANGES TO DATABASE
            sql = "UPDATE tbl_stud_info \
        SET Last_Name=%s,First_Name=%s,Middle_Name=%s,Home_Address=%s,\
        Email_Address=%s, Age=%s, Birthday=%s, Gender=%s, Course=%s WHERE Student_ID=%s"
            data = (strLName, strFName, strMName, strHomeAdd,
                    strEmailAdd,strAge, strBirthday, strGender, strCourse , strID)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            flash('Record successfully edited in the database!')
            return redirect('/read_all_stud')

        else:
            return 'Error while updating student'
    except Exception as e:
        print (e)
        return str(e), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/delete_stud/<string:id>')
def delete_stud(id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tbl_stud_info WHERE Student_ID=%s", (id,))
        conn.commit()
        flash('Record successfully deleted in the database')
        return redirect('/read_all_stud')
    except Exception as e:
        print (e)
        return str(e), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    app.run(debug=True, port=5050)