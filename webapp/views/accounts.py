from flask import Blueprint, flash, render_template, redirect, request, url_for
from flask_login import login_required, login_user, logout_user, current_user


from .. import bcrypt, db
from webapp.models.user_model import User
from webapp.form import LoginForm, RegisterForm

accounts_bp = Blueprint("accounts", __name__)


@accounts_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in.", "info")
        return redirect(url_for("home.home"))
    form = LoginForm(request.form)

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("home.home"))
        flash("Invalid email and/or password.", "danger")

    return render_template("accounts/login.html", form=form)


@accounts_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        flash("You are already registered.", "info")
        return redirect(url_for("home.home"))
    form = RegisterForm(request.form)
    
    if form.validate_on_submit():
        user = User(full_name=form.fullname.data, username=form.username.data, 
                    email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash("You registered and are now logged in. Welcome!", "success")

        return redirect(url_for("home.home"))

    return render_template("accounts/register.html", form=form)


@accounts_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You were logged out.", "success")
    return redirect(url_for("accounts.login"))
