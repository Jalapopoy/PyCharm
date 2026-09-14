from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # GET USER INPUT
        strIDJEM = request.form["Patient_ID"]
        strNameJEM = request.form["Patient_Name"]
        dblAgeJEM = float(request.form["Age"])
        dblRTypeJEM = request.form["Room_Type"]
        dblRPDayJEM = float(request.form["Rate_Per_Day"])
        dblNDaysJEM = float(request.form["No_Of_Days"])
        dblLChargesJEM = float(request.form["Laboratory_Charges"])
        dblEChargesJEM = float(request.form["Extra_Charges"])

        # PROCESS INPUTS - COMPUTATION
        dblRChargesJEM = dblRPDayJEM * dblNDaysJEM
        dblTAmountJEM = dblRChargesJEM + dblLChargesJEM + dblEChargesJEM
        dblHInsuranceJEM = dblTAmountJEM * 0.05
        dblPHealthJEM = dblTAmountJEM * 0.06
        dblSSSJEM = dblTAmountJEM * 0.07
        dblTDiscountJEM = dblHInsuranceJEM + dblPHealthJEM + dblSSSJEM
        dblAPayJEM = dblTAmountJEM - dblTDiscountJEM

        # Determine Age Group
        if dblAgeJEM <= 2:
            strAGroupJEM = "Babies"
        elif dblAgeJEM <= 16:
            strAGroupJEM = "Children"
        elif dblAgeJEM <= 30:
            strAGroupJEM = "Young Adults"
        elif dblAgeJEM <= 45:
            strAGroupJEM = "Middle Aged Adults"
        else:
            strAGroupJEM = "Old Adults"

        strOutput = "<h3>HOSPITAL BILL</h3>" \
                    "Patient Number: " + strIDJEM + "<br>" \
                    "Patient Name: " + strNameJEM + "<br>" \
                    "Age: " + dblAgeJEM + "<br>" \
                    "Age Group: " + strAGroupJEM + "<br>" \
                    "Room Type: " + dblRTypeJEM + "<br>" \
                    "Rate Per Day: " + dblRPDayJEM + "<br>" \
                    "No. Of Days: " + dblNDaysJEM + "<br>" \
                    "Laboratory Charges: " + dblLChargesJEM + "<br>" \
                    "Extra Charges: " + dblEChargesJEM + "<br>" \
                    "Room Charge: " + dblRChargesJEM + "<br>" \
                    "Total Amount: " + dblTAmountJEM + "<br>" \
                    "Health Insurance: " + dblHInsuranceJEM + "<br>" \
                    "PhilHealth: " + dblPHealthJEM + "<br>" \
                    "SSS: " + dblSSSJEM + "<br>" \
                    "<br>"

        return strOutput

    return render_template("mp1-mod3-sia101-jem.html")


if __name__ == "__main__":
    app.run(debug=True, port=8000)
