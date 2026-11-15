import pymysql
from app import app
from db_config import mysql
from flask import flash, render_template, request, redirect

#View Read-All Page
@app.route('/read_all_stud')
def read_all_stud():
    connJEM = None
    cursorJEM = None
    try:
        connJEM = mysql.connect()
        cursorJEM = connJEM.cursor(pymysql.cursors.DictCursor)
        cursorJEM.execute("SELECT * FROM tbl_stud_info")
        rowsJEM = cursorJEM.fetchall()
        return render_template('readstuds.html', rows=rowsJEM)
    except Exception as eJEM:
        print(eJEM)
        return str(eJEM), 500
    finally:
        cursorJEM.close()
        connJEM.close()

@app.route('/create_stud_view')
def create_stud_view():
    return render_template('addstuds.html')

#POST METHOD to Save New Student Record
@app.route('/create_stud', methods=['POST'])
def create_stud():
    connJEM = None
    cursorJEM = None
    try:
        strid = request.form['StudID']
        strLNameJEM = request.form['LastName']
        strFNameJEM = request.form['FirstName']
        strMNameJEM = request.form['MiddleName']
        strHomeAddJEM = request.form['Address']
        strEmailAddJEM = request.form['EmailAdd']
        strAgeJEM = request.form['Age']
        strBirthdayJEM = request.form['Birthday']
        strGenderJEM = request.form['Gender']
        strCourseJEM = request.form['Course']

        if request.method == 'POST':
            sqlJEM = "INSERT INTO tbl_stud_info \
                (Student_ID, Last_Name, First_Name, Middle_Name, Home_Address, \
                 Email_Address,Age, Birthday, Gender, Course) \
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            dataJEM = (strid, strLNameJEM, strFNameJEM, strMNameJEM, strHomeAddJEM, strEmailAddJEM, strAgeJEM, strBirthdayJEM, strGenderJEM, strCourseJEM)
            connJEM = mysql.connect()
            cursorJEM = connJEM.cursor()
            cursorJEM.execute(sqlJEM, dataJEM)
            connJEM.commit()
            flash('Record successfully saved in the database')
            return redirect('/read_all_stud')
        else:
            return 'Error while adding student'
    except Exception as eJEM:
        print(eJEM)
        return str(eJEM), 500
    finally:
        cursorJEM.close()
        connJEM.close()


#View Read-One Page
@app.route('/read_one_stud/<string:id>')
def read_one_stud(id):
    connJEM = None
    cursorJEM = None
    try:
        connJEM = mysql.connect()
        cursorJEM = connJEM.cursor(pymysql.cursors.DictCursor)
        cursorJEM.execute("SELECT * FROM tbl_stud_info WHERE student_id=%s", id)
        rowJEM = cursorJEM.fetchone()
        if rowJEM:
            return render_template('viewstuds.html', row=rowJEM)
        else:
            return 'Error loading #{id}'.format(id=id)
    except Exception as eJEM:
        print(eJEM)
        return str(eJEM), 500
    finally:
        cursorJEM.close()
        connJEM.close()

#View Update Page
@app.route('/update_stud_view/<string:id>')
def update_stud_view(id):
    connJEM = None
    cursorJEM = None
    try:
        connJEM = mysql.connect()
        cursorJEM = connJEM.cursor(pymysql.cursors.DictCursor)
        cursorJEM.execute("SELECT * FROM tbl_stud_info WHERE Student_ID=%s", id)
        rowJEM = cursorJEM.fetchone()
        if rowJEM:
            return render_template('editstuds.html', row=rowJEM)
        else:
            return 'Error loading #{id}.format(id=id)'
    except Exception as eJEM:
        print(eJEM)
        return str(eJEM), 500
    finally:
        cursorJEM.close()
        connJEM.close()

#POST Method to Save Changes in data
@app.route('/update_stud', methods=['POST'])
def update_stud():
    connJEM = None
    cursorJEM = None
    try:
        # GET STUDENT INPUTS
        stridJEM = request.form['StudID']
        strLNameJEM = request.form['LastName']
        strFNameJEM = request.form['FirstName']
        strMNameJEM = request.form['MiddleName']
        strHomeAddJEM = request.form['Address']
        strEmailAddJEM = request.form['EmailAdd']
        strAgeJEM = request.form['Age']
        strBirthdayJEM = request.form['Birthday']
        strGenderJEM = request.form['Gender']
        strCourseJEM = request.form['Course']

        if request.method == 'POST':
            #SAVE CHANGES TO DATABASE
            sqlJEM = "UPDATE tbl_stud_info \
        SET Last_Name=%s,First_Name=%s,Middle_Name=%s,Home_Address=%s,\
        Email_Address=%s, Age=%s, Birthday=%s, Gender=%s, Course=%s WHERE Student_ID=%s"
            dataJEM = (strLNameJEM, strFNameJEM, strMNameJEM, strHomeAddJEM,
                       strEmailAddJEM, strAgeJEM, strBirthdayJEM, strGenderJEM, strCourseJEM, stridJEM)
            connJEM = mysql.connect()
            cursorJEM = connJEM.cursor()
            cursorJEM.execute(sqlJEM, dataJEM)
            connJEM.commit()
            flash('Record successfully edited in the database!')
            return redirect('/read_all_stud')

        else:
            return 'Error while updating student'
    except Exception as eJEM:
        print (eJEM)
        return str(eJEM), 500
    finally:
        cursorJEM.close()
        connJEM.close()

@app.route('/delete_stud/<string:id>')
def delete_stud(id):
    connJEM = None
    cursorJEM = None
    try:
        connJEM = mysql.connect()
        cursorJEM = connJEM.cursor()
        cursorJEM.execute("DELETE FROM tbl_stud_info WHERE Student_ID=%s", (id,))
        connJEM.commit()
        flash('Record successfully deleted in the database')
        return redirect('/read_all_stud')
    except Exception as eJEM:
        print (eJEM)
        return str(eJEM), 500
    finally:
        cursorJEM.close()
        connJEM.close()

if __name__ == "__main__":
    app.run(debug=True, port=5050)