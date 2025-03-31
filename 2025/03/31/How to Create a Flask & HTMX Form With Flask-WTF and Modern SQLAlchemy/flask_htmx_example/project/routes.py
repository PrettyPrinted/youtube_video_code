from flask import Blueprint, render_template
from sqlalchemy import select

from .forms import PhoneNumbersForm
from .extensions import db
from .models import PhoneNumber

main = Blueprint('main', __name__)

@main.route('/')
def index():
    stmt = select(PhoneNumber)
    phone_numbers = db.session.scalars(stmt).all()
    data = {"phone_numbers": phone_numbers}
    form = PhoneNumbersForm(data=data)
    return render_template('index.html', form=form)

@main.route('/save', methods=["POST"])
def save():
    stmt = select(PhoneNumber)
    phone_numbers = db.session.scalars(stmt).all()
    data = {"phone_numbers": phone_numbers}
    form = PhoneNumbersForm(data=data)

    if form.validate_on_submit():
        for phone_number in form.phone_numbers:
            if phone_number.form.id.data:
                stmt = select(PhoneNumber).where(PhoneNumber.id == phone_number.form.id.data)
                pn = db.session.execute(stmt).scalar()

                pn.phone_type = phone_number.phone_type.data
                pn.country_code = phone_number.country_code.data
                pn.area_code = phone_number.area_code.data
                pn.number = phone_number.number.data
                
            else:
                pn = PhoneNumber(
                    phone_type=phone_number.phone_type.data,
                    country_code=phone_number.country_code.data,
                    area_code=phone_number.area_code.data,
                    number=phone_number.number.data
                )

                db.session.add(pn)
        db.session.commit()

        stmt = select(PhoneNumber)
        phone_numbers = db.session.scalars(stmt).all()
        data = {"phone_numbers": phone_numbers}
        form = PhoneNumbersForm(data=data)
        return render_template("form.html", form=form)

@main.route('/add_phone_number')
def add_phone_number():
    stmt = select(PhoneNumber)
    phone_numbers = db.session.scalars(stmt).all()
    data = {"phone_numbers": phone_numbers}
    form = PhoneNumbersForm(data=data)
    form.phone_numbers.append_entry()
    return render_template("form.html", form=form)

@main.route("/delete/<int:id>", methods=["DELETE", "GET"])
def delete(id=None):
    if id:
        stmt = select(PhoneNumber).where(PhoneNumber.id == id)
        pn = db.session.execute(stmt).scalar()
        db.session.delete(pn)
        db.session.commit()

    stmt = select(PhoneNumber)
    phone_numbers = db.session.scalars(stmt).all()
    data = {"phone_numbers": phone_numbers}
    form = PhoneNumbersForm(data=data)
    return render_template("form.html", form=form)