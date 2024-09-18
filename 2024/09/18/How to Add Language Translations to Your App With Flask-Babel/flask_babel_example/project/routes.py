from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for

from .extensions import db
from .models import Reservation

main = Blueprint("main", __name__)

@main.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        reservation = Reservation(
            name=request.form.get("name"), 
            date=datetime.strptime(request.form.get("date"), "%Y-%m-%d"),
            guests=request.form.get("guests"), 
            nights=request.form.get("nights"), 
            room=request.form.get("room"), 
            amount=request.form.get("amount"), 
            currency=request.form.get("currency")
        )
        db.session.add(reservation)
        db.session.commit()

        return redirect(url_for("main.index"))
    
    reservations = Reservation.query.order_by(Reservation.date).all()

    return render_template("index.html", reservations=reservations)