from flask import Blueprint, abort, flash, render_template, redirect, request
from flask.helpers import url_for
from flask_login import current_user, login_required
from my_flask import db
from my_flask.customers.forms import CustomerForm
from my_flask.models import Customer, CustomerNotes


customers = Blueprint("customers", __name__)


@customers.get("/customers")
@login_required
def customers_page():
    page = request.args.get("page", 1, type=int)
    customers = (
        Customer.query.filter_by(user_id=current_user.id)
        .order_by(Customer.date_created.desc())
        .paginate(page=page, per_page=15)
    )
    return render_template(
        "customers/customers_table.html", title="Customers", customers=customers
    )


@customers.route("/customers/new", methods=["GET", "POST"])
@login_required
def add_customer():
    statuses = ["NEW", "OFFER_SENT", "LOST", "WIN"]
    form = CustomerForm()
    if form.validate_on_submit():
        customer = Customer(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            status=form.status.data,
            company=form.company.data,
            email=form.email.data,
            user_id=current_user.id,
        )
        db.session.add(customer)
        db.session.commit()
        flash(
            f"Customer {form.first_name.data} {form.last_name.data} created successfully",
            category="success",
        )
        return redirect(url_for("customers.customers_page"))
    return render_template(
        "customers/add_customer.html",
        form=form,
        button_value="Add",
        statuses=statuses,
        legend="New Customer",
    )


@customers.get("/customers/<int:customer_id>")
@login_required
def customer_info(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    if customer.manager != current_user:
        abort(403)

    comments = CustomerNotes.query.filter_by(
        customer_id=customer_id, note_type="comment"
    )
    call_logs = CustomerNotes.query.filter_by(
        customer_id=customer_id, note_type="call log"
    )
    meeting_logs = CustomerNotes.query.filter_by(
        customer_id=customer_id, note_type="meeting log"
    )
    print(comments)
    return render_template(
        "customers/customer.html",
        customer=customer,
        comments=comments,
        call_logs=call_logs,
        meeting_logs=meeting_logs,
    )


@customers.route("/customers/<int:customer_id>/update", methods=["GET", "POST"])
@login_required
def update_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    if customer.manager != current_user:
        abort(403)
    statuses = ["NEW", "OFFER_SENT", "LOST", "WIN"]
    form = CustomerForm()
    if form.validate_on_submit():
        customer.first_name = form.first_name.data
        customer.last_name = form.last_name.data
        customer.status = form.status.data
        customer.company = form.company.data
        customer.email = form.email.data
        db.session.commit()
        flash("Customer has been updated", category="success")
        return redirect(url_for("customers.customer_info", customer_id=customer.id))
    elif request.method == "GET":
        form.first_name.data = customer.first_name
        form.last_name.data = customer.last_name
        form.status.data = customer.status
        form.company.data = customer.company
        form.email.data = customer.email

    return render_template(
        "customers/add_customer.html",
        customer=customer,
        form=form,
        button_value="Update",
        legend="Update Customer",
        statuses=statuses,
    )


@customers.post("/customers/<int:customer_id>/delete")
@login_required
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    if customer.manager != current_user:
        abort(403)
    db.session.delete(customer)
    db.session.commit()
    flash("Customer has been deleted", category="warning")
    return redirect(url_for("customers.customers_page"))
