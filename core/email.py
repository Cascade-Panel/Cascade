from mailbuddy import Email
from sanic import Sanic

from core.database.models.user.User import User

def welcome_email(app: Sanic, user: User):
    welcome = Email(
        host=app.ctx.env_manager.get("SMTP_HOST"),
        port=app.ctx.env_manager.get("SMTP_PORT"),
        sender=app.ctx.env_manager.get("SMTP_SENDER"),
    )

    welcome.plain_body("Welcome to the platform, {first-name}!")

    welcome.add_html_body_from_file("./templates/email/welcome.html")

    welcome.add_format_variables({
        "first-name": user.first_name,
        "last-name": user.last_name,
        "email": user.email,
        "avatar": user.avatar
    })

    welcome.send(user.email)