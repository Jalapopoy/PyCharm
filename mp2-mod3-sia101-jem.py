from flask import Flask, render_template
from flask import request
app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # GET USER INPUT
        strIDJEM = request.form["StudentID"]
        strLNameJEM = request.form["LastName"]
        strFNameJEM = request.form["FirstName"]
        strMNameJEM = request.form["MiddleName"]
        strGenderJEM = request.form["Gender"]
        strEmailJEM = request.form["Email"]
        strCourseJEM = request.form["Course"]

        # GET SELECT RADIOBUTTON
        strTuitionJEM = request.form["tuition"]
        if strTuitionJEM == "1st Year 500.00":
            tuition = 500
        elif strTuitionJEM == "2nd Year 600.00":
            tuition = 600
        elif strTuitionJEM == "3rd Year 800.00":
            tuition = 800
        elif strTuitionJEM == "4th Year 900.00":
            tuition = 900

        # GET SELECTED CHECKBOXES
        if request.form.get("rfee", False):
            rfee = 100
        else:
            rfee = 0

        if request.form.get("ifee", False):
            ifee = 100
        else:
            ifee = 0

        if request.form.get("idfee", False):
            idfee = 100
        else:
            idfee = 0

        if request.form.get("lfee", False):
            lfee = 50
        else:
            lfee = 0

        # GET SELECTED DRINKS
        strScholarship = request.form["scholarship"]
        if strScholarship == "DEAN'S LISTER 200.00":
            scholarship = 200
        elif strScholarship == "STUDENT ASSISTANT 500.00":
            scholarship = 500
        elif strScholarship == "PRESIDENT LIST 700.00":
            scholarship = 700
        elif strScholarship == "FULL SCHOLARSHIP 1000.00":
            scholarship = 1000

        total = tuition + rfee + ifee + idfee + lfee - scholarship

        strOutput = "<h3>OFFICIAL RECEIPT</h3>"
        strOutput += "Student ID: " + strIDJEM + "<br>"
        strOutput += "Student Name: " + strLNameJEM + ", " + strFNameJEM + " " + strMNameJEM + "<br>"
        strOutput += "Student Gender: " + strGenderJEM + "<br>"
        strOutput += "Student Email: " + strEmailJEM + "<br>"
        strOutput += "Student Course: " + strCourseJEM + "<br>"
        strOutput += "Total Amount: " + str(total) + "<br>"

        return strOutput

    return render_template("mp2-mod3-sia101-jem.html")

if __name__ == "__main__":
    app.run(debug=True, port=8000)
