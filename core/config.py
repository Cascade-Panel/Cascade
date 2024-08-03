""" A module to manage the configuration of the application. """

from sanic import Sanic
from core.database.models.Config import Config
from core.database.DALs.config_dal import ConfigDAL

CONFIG_VALUES = [
    # ['config_name', 'config_type', 'default_value', 'description']
    ## Application configuration ##
    ['APP_NAME', 'str', 'BlendPanel' 'The name of the application.'],
    ['APP_DESC', 'str', 'A simple and secure panel for managing your servers.', 'The description of the application.'],

    ## Email server configuration ##
    ['EMAIL_HOST', 'str', 'smtp.gmail.com', 'The SMTP server host.'],
    ['EMAIL_PORT', 'int', 587, 'The SMTP server port.'],
    ['EMAIL_SENDER', 'str', 'The email address to send emails from.', 'The email address to send emails from.'],
     
    ## Email templates ##
    ['EMAIL_WELCOME_SUBJECT', 'str', 'Welcome to BlendPanel!', 'The subject of the welcome email.'],
    ['EMAIL_WELCOME_PLAIN_BODY', 'str', 'Welcome to BlendPanel, {first-name}!', 'The plain text body of the welcome email.'],
    ['EMAIL_WELCOME_HTML_BODY', 'str', '<h1>Welcome to BlendPanel, {first-name}!</h1>', 'The string HTML body of the welcome email.'],

    ['EMAIL_PASSWORD_RESET_SUBJECT', 'str', 'Password Reset Request', 'The subject of the password reset email.'],
    ['EMAIL_PASSWORD_RESET_PLAIN_BODY', 'str', 'You have requested a password reset. {reset-url}', 'The plain text body of the password reset email.'],
    ['EMAIL_PASSWORD_RESET_HTML_BODY', 'str', '<h1>Password Reset Request</h1><p>Please click the <a href="{reset-url}">link</a>', 'The string HTML body of the password reset email.'],

    ['EMAIL_VERIFICATION_SUBJECT', 'str', 'Email Verification', 'The subject of the email verification email.'],
    ['EMAIL_VERIFICATION_PLAIN_BODY', 'str', 'Please verify your email address by clicking the link below: {verification-url}', 'The plain text body of the email verification email.'],
    ['EMAIL_VERIFICATION_HTML_BODY', 'str', '<h1>Email Verification</h1><p>Please verify your email address by clicking the <a href="{verification-url}">link</a>', 'The string HTML body of the email verification email.'],

    ['EMAIL_LOGIN_CODE_SUBJECT', 'str', 'Login Code', 'The subject of the login code email.'],
    ['EMAIL_LOGIN_CODE_PLAIN_BODY', 'str', 'Your login code is: {login-code-url}', 'The plain text body of the login code email.'],
    ['EMAIL_LOGIN_CODE_HTML_BODY', 'str', '<h1>Login Code</h1><p>Your login code url is: {login-code-url}', 'The string HTML body of the login code email.'],
]

async def update_config_value(app: Sanic, key: str, value: str | int | bool) -> None:
    """
    Update a configuration value in the database.

    Attributes:
        app (sanic.Sanic): The application instance.
        key (str): The key of the configuration value to update.
        value (str | int | bool): The new value of the configuration.
    """
    async with app.ctx.asyncsession as session:
        async with session.begin():
            config_dal = ConfigDAL(session)

            config_data = config_dal.get(key=key)

            if not config_data:
                raise ValueError(f"Configuration value not found: {key}")
            
            if config_data.type == 'bool':
                if type(value) != bool:
                    raise ValueError(f"Invalid type for configuration value: {config_data.type}")
            elif config_data.type == 'int':
                if type(value) != int:
                    raise ValueError(f"Invalid type for configuration value: {config_data.type}")
            elif config_data.type == 'str':
                if type(value) != str:
                    raise ValueError(f"Invalid type for configuration value: {config_data.type}")
            else:
                raise ValueError(f"Invalid type for configuration value: {config_data.type}")

            new_value = await config_dal.update(key, value)
            app.config[key] = new_value

async def init_config(app):
    """
    Initialize the configuration of the application.

    Attributes:
        app (sanic.Sanic): The application instance.
    """
    async with app.ctx.asyncsession as session:
        async with session.begin():
            config_dal = ConfigDAL(session)

            for config_value in CONFIG_VALUES:
                if not await config_dal.get_by_name(config_value[0]):
                    await config_dal.new(config_value[0], config_value[1], config_value[2], config_value[3])
                app.config[config_value[0]] = await config_dal.get(config_value[0])
    
    app.ctx.config = type('', (), {})()
    app.ctx.config.update = update_config_value