from flask import Blueprint, render_template
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired, Length

bp = Blueprint("auth", __name__)


class NameForm(FlaskForm):
    username = StringField(
        "用户名: ",
        validators=[
            DataRequired(),
            Length(4, 20),
        ],
    )
    password = PasswordField("密码：", validators=[DataRequired(), Length(4, 20)])
    submit = SubmitField("登录")


@bp.route("/login/", methods=["GET", "POST"])
def login():
    username = None
    form = NameForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        print(f"用户名> {username} | 密码> {password} ")
    return render_template("auth/login.html", form=form)
