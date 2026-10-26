from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # GET USER INPUT
        strIDJEM = request.form["Patient_ID"]
        strNameJEM = request.form["Patient_Name"]
        dblAgeJEM = float(request.form["Age"])
        strRTypeJEM = request.form["Room_Type"]
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

        if strRTypeJEM == "W":
            strRDescJEM = "Ward"
        elif strRTypeJEM == "SPR":
            strRDescJEM = "Semi Private Room"
        elif strRTypeJEM == "PR":
            strRDescJEM = "Private Room"
        elif strRTypeJEM == "ER":
            strRDescJEM = "Encubator Room"
        elif strRTypeJEM == "ICU":
            strRDescJEM = "Intensive Care Unit"
        elif strRTypeJEM == "NICU":
            strRDescJEM = "Neonatal Intensive Care Unit"
        elif strRTypeJEM == "PICU":
            strRDescJEM = "Pediatric Intensive Care Unit"
        elif strRTypeJEM == "IC":
            strRDescJEM = "Incubator Cost"
        else:
            strRDescJEM = "Unavailable Room"

        strOutput = (
            f"<h3>HOSPITAL BILL</h3>"
            f"Patient Number: {strIDJEM}<br>"
            f"Patient Name: {strNameJEM}<br>"
            f"Age: {dblAgeJEM}<br>"
            f"Age Group: {strAGroupJEM}<br>"
            f"Room Type: {strRTypeJEM}<br>"
            f"Room Description: {strRDescJEM}<br>"
            f"Rate Per Day: {dblRPDayJEM}<br>"
            f"No. Of Days: {dblNDaysJEM}<br>"
            f"Laboratory Charges: {dblLChargesJEM}<br>"
            f"Extra Charges: {dblEChargesJEM}<br>"
            f"Room Charge: {dblRChargesJEM}<br>"
            f"Total Amount: {dblTAmountJEM}<br>"
            f"Health Insurance: {dblHInsuranceJEM}<br>"
            f"PhilHealth: {dblPHealthJEM}<br>"
            f"SSS: {dblSSSJEM}<br>"
            f"Total Discount: {dblTDiscountJEM}<br>"
            f"Amount to Pay: {dblAPayJEM}<br>"
        )

        return strOutput

    return render_template("mp1-mod3-sia101-jem.html")


if __name__ == "__main__":
    app.run(debug=True, port=8000)
