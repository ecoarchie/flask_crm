from flask.helpers import url_for
from werkzeug.utils import redirect
from my_flask import db
from flask import flash
from my_flask.models import Customer
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from my_flask.customers.forms import AddCustomerForm

customers = Blueprint("customers", __name__)


@customers.route("/customers")
@login_required
def customers_page():
    return render_template("customers/customers.html", title="Customers")


@customers.route("/add_customer", methods=["GET", "POST"])
def add_customer():
    statuses = ["NEW", "OFFER_SENT", "LOST", "WIN"]
    form = AddCustomerForm()
    if form.validate_on_submit():
        customer = Customer(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            status=form.status.data,
            company=form.company.data,
            email=form.email.data,
            manager_id=current_user.id,
        )
        db.session.add(customer)
        db.session.commit()
        flash(
            f"Customer {form.first_name.data} {form.last_name.data} created successfully",
            category="success",
        )
        return redirect(url_for("customers.customers_page"))
    return render_template("customers/add_customer.html", form=form, statuses=statuses)
