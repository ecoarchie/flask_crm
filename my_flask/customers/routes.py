from flask import Blueprint, render_template

customers = Blueprint("customers", __name__)


@customers.route("/customers")
def customers_page():
    return render_template("customers.html", title="Customers")
