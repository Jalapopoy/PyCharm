from flask import Flask, render_template
from flask import request
app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # GET USER INPUT
        strID = request.form["CustomerID"]
        strName = request.form["CustomerName"]

        # GET SELECT RADIOBUTTON
        strOrder = request.form["order"]
        if strOrder == "Hamburger":
            orders = 50
        elif strOrder == "Cheese Burger":
            orders = 100
        elif strOrder == "Big MacJabee":
            orders = 150

        # GET SELECTED CHECKBOXES
        if request.form.get("patty", False):
            patty = 25
        else:
            patty = 0

        if request.form.get("coles", False):
            coles = 50
        else:
            coles = 0

        if request.form.get("hamegg", False):
            hamegg = 100
        else:
            hamegg = 0

        # GET SELECTED DRINKS
        strDrinks = request.form["drinks"]
        if strDrinks == "SOFTDRINKS 30.00":
            drinks = 30
        elif strDrinks == "COFFEE 40.00":
            drinks = 40
        elif strDrinks == "MANGO JUICE 50.00":
            drinks = 50

        total = orders + patty + coles + hamegg + drinks

        strOutput = "<h3>OFFICIAL RECEIPT</h3>"
        strOutput += "Customer ID: " + strID + "<br>"
        strOutput += "Customer Name: " + strName + "<br>"
        strOutput += "Total Amount: " + str(total) + "<br>"

        return strOutput

    return render_template("act3-mod3-sia101-jem.html")

if __name__ == "__main__":
    app.run(debug=True, port=8000)
