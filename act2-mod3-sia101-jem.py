from flask import Flask, render_template
from flask import request
app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # GET USER INPUT
        strID = request.form["Student_ID"]
        strName = request.form["Student_Name"]
        dblPre = request.form["Prelim_Grade"]
        dblMid = request.form["Midterm_Grade"]
        dblFin = request.form["Final_Grade"]

        # PROCESS INPUTS - COMPUTATION
        dblSGrade = (float(dblPre) + float(dblMid) + float(dblFin)) / 3

        # Apply If and Else Statement to determine Remarks
        if dblSGrade > 74:
            strRemarks = "Passed!"
        else:
            strRemarks = "Failed"

        # Apply If and Elif Statement to determine Ratings
        if dblSGrade > 97 and dblSGrade <= 100:
            strRatings = "Excellent!"
        elif dblSGrade > 91 and dblSGrade <= 97:
            strRatings = "Very Good!"
        elif dblSGrade > 82 and dblSGrade <= 91:
            strRatings = "Good!"
        elif dblSGrade > 77 and dblSGrade <= 82:
            strRatings = "Fair!"
        elif dblSGrade >= 75 and dblSGrade <= 77:
            strRatings = "Satisfactory!"
        else:
            strRatings = "Poor!"

        strOutput = "<h3>GRADE SLIP</h3>" \
                    "Student Number: " + strID + "<br>" \
                                                 "Student Name: " + strName + "<br>" \
                                                                              "Prelim Grade: " + dblPre + "<br>" \
                                                                                                          "Midterm Grade: " + dblMid + "<br>" \
                                                                                                                                       "Final Grade: " + dblFin + "<br>" \
                                                                                                                                                                  "Subject Grade: " + str(
            dblSGrade) + "<br>" \
                         "Remarks: " + strRemarks + "<br>" \
                                                    "Ratings: " + strRatings + "<br>"

        return strOutput

    return render_template("act2-mod3-sia101-jem.html")


if __name__ == "__main__":
    app.run(debug=True, port=8000)
