from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField
from wtforms.fields.simple import StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from webapp.models.user_model import User


class RegisterForm(FlaskForm):
    full_name = StringField('Full Name', validators=[])
    username = StringField('Username')
    email = EmailField(
        "Email", validators=[DataRequired(), Email(message=None), Length(min=6, max=40)]
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        "Repeat password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
    )

    def validate(self, **kwargs):
        initial_validation = super(RegisterForm, self).validate(**kwargs)
        if not initial_validation:
            return False

        user = User.query.filter_by(email=self.email.data).first()
        if user:
            if not isinstance(self.email.errors, list):
                self.email.errors = []
            self.email.errors.append("Email already registered")
            return False

        if self.password.data != self.confirm.data:
            if not isinstance(self.password.errors, list):
                self.password.errors = []
            self.password.errors.append("Passwords must match")
            return False

        return True


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
