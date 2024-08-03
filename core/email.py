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
            host=app.config['EMAIL_HOST'],
            port=app.config['EMAIL_PORT'],
            sender=app.config['EMAIL_SENDER'],
        )

        welcome.add_plain_body(app.config['EMAIL_WELCOME_PLAIN_BODY'])

        welcome.add_html_body(app.config['EMAIL_WELCOME_HTML_BODY'])

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
            host=app.config['EMAIL_HOST'],
            port=app.config['EMAIL_PORT'],
            sender=app.config['EMAIL_SENDER'],
        )

        password_reset.plain_body(app.config['EMAIL_PASSWORD_RESET_PLAIN_BODY'])

        password_reset.add_html_body(app.config['EMAIL_PASSWORD_RESET_HTML_BODY'])

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
            host=app.config['EMAIL_HOST'],
            port=app.config['EMAIL_PORT'],
            sender=app.config['EMAIL_SENDER'],
        )

        email_verification.plain_body(app.config['EMAIL_VERIFICATION_PLAIN_BODY'])

        email_verification.add_html_body(app.config['EMAIL_VERIFICATION_HTML_BODY'])

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
            host=app.config['EMAIL_HOST'],
            port=app.config['EMAIL_PORT'],
            sender=app.config['EMAIL_SENDER'],
        )

        email_code_login.plain_body(app.config['EMAIL_LOGIN_CODE_PLAIN_BODY'])

        email_code_login.add_html_body(app.config['EMAIL_LOGIN_CODE_HTML_BODY'])

        email_code_login.add_format_variables({
            "first-name": user.first_name,
            "last-name": user.last_name,
            "email": user.email,
            "avatar": user.avatar,
            "login-code-url": login_code_url
        })

        email_code_login.send(user.email)
        return email_code_login