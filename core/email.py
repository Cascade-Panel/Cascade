from mailbuddy import Email
from sanic import Sanic

from core.database.models.user.User import User

class Emails:
    @staticmethod
    def welcome(app: Sanic, user: User) -> Email:
        """
            Send a welcome email to the user.

            Attributes:
                app (Sanic): The Sanic application.
                user (User): The user.

            Returns:
                Email: The email object.
        """
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
        return welcome
    
    @staticmethod
    def password_reset(app: Sanic, user: User, reset_url: str) -> Email:
        """
            Send a password reset email to the user.

            Attributes:
                app (Sanic): The Sanic application.
                user (User): The user.
                reset_url (str): The URL to reset the password.

            Returns:
                Email: The email object.
        """
        password_reset = Email(
            host=app.ctx.env_manager.get("SMTP_HOST"),
            port=app.ctx.env_manager.get("SMTP_PORT"),
            sender=app.ctx.env_manager.get("SMTP_SENDER"),
        )

        password_reset.plain_body("You have requested a password reset. Please click the link below to reset your password. {reset-url}")

        password_reset.add_html_body_from_file("./templates/email/password-reset.html")

        password_reset.add_format_variables({
            "first-name": user.first_name,
            "last-name": user.last_name,
            "email": user.email,
            "avatar": user.avatar,
            "reset-url": reset_url
        })

        password_reset.send(user.email)
        return password_reset
    
    @staticmethod
    def email_verification(app: Sanic, user: User, verification_url: str) -> Email:
        """
            Send an email verification email to the user.

            Attributes:
                app (Sanic): The Sanic application.
                user (User): The user.
                verification_url (str): The URL to verify the email.

            Returns:
                Email: The email object.
        """
        email_verification = Email(
            host=app.ctx.env_manager.get("SMTP_HOST"),
            port=app.ctx.env_manager.get("SMTP_PORT"),
            sender=app.ctx.env_manager.get("SMTP_SENDER"),
        )

        email_verification.plain_body("Please click the link below to verify your email. {verification-url}")

        email_verification.add_html_body_from_file("./templates/email/email-verification.html")

        email_verification.add_format_variables({
            "first-name": user.first_name,
            "last-name": user.last_name,
            "email": user.email,
            "avatar": user.avatar,
            "verification-url": verification_url
        })

        email_verification.send(user.email)
        return email_verification
    
    @staticmethod
    def email_code_login(app: Sanic, user: User, login_code_url: str) -> Email:
        """
            Send an email verification code to the user.

            Attributes:
                app (Sanic): The Sanic application.
                user (User): The user.
                login_code_url (str): The URL to login with the code.

            Returns:
                Email: The email object.
        """
        email_code_login = Email(
            host=app.ctx.env_manager.get("SMTP_HOST"),
            port=app.ctx.env_manager.get("SMTP_PORT"),
            sender=app.ctx.env_manager.get("SMTP_SENDER"),
        )

        email_code_login.plain_body("Your login code is: {login-code-url}")

        email_code_login.add_format_variables({
            "first-name": user.first_name,
            "last-name": user.last_name,
            "email": user.email,
            "avatar": user.avatar,
            "login-code-url": login_code_url
        })

        email_code_login.send(user.email)
        return email_code_login