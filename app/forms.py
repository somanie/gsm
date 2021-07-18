from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, InputRequired, EqualTo, Email, ValidationError
from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[Length(min=5, max=30), DataRequired()])
    email = StringField("Email", validators=[Email()])
    password = PasswordField("Password", validators=[Length(min=8), InputRequired()])
    password_confirm = PasswordField("Confirm Password", validators=[Length(min=8), EqualTo("password", message="Passwords must match")])
    sign_in = BooleanField("Sign me in afterwards")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username already taken.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email already taken.")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    remember_me = BooleanField("Remember Me")

    def validate(self, *args, **kwargs):
        valid = super(LoginForm, self).validate(*args, **kwargs)
        
        if valid:
            user = User.query.filter_by(username=self.username.data).first()
            if user:
                check = user.check_password(self.password.data)
                if not check:
                    self.password.errors.append("Invalid login details")
            else:
                self.password.errors.append("Invalid login details")
                
        return valid and not self.password.errors


# class ForgotPasswordForm(FlaskForm):
#     email = StringField("Email", validators=[Email()])

#     def validate_email(self, email):
#         user = User.query.filter_by(email=email.data).first()
#         if not user:
#             raise ValidationError("Email not registered with any account.")


# class ResetPasswordForm(FlaskForm):
#     password = PasswordField("Password", validators=[Length(min=8), InputRequired()])
#     password_confirm = PasswordField("Confirm Password", validators=[Length(min=8), EqualTo("password", message="Passwords must match")])

#     def validate(self, *args, **kwargs):
#         valid = super(ResetPasswordForm, self).validate(*args, **kwargs)
        
#         if self.user.check_password(self.password.data):
#             self.password.errors.append("You must set a new password")
#         return valid and not self.errors