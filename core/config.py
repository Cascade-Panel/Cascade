""" A module to manage the configuration of the application. """

from sanic import Sanic
from core.database.models.Config import Config
from core.database.DALs.config_dal import ConfigDAL

CONFIG_VALUES = [
   # ['config_name', 'config_type', 'default_value', 'description']
    ['app_name', 'str', 'BlendPanel' 'The name of the application.']
]

async def get_config_value(app: Sanic, key: str) -> str:
    """
    Retrieve a configuration value from the database.

    Attributes:
        app (sanic.Sanic): The application instance.
        key (str): The name of the configuration value to retrieve.

    Returns:
        str: The value of the configuration.
    """
    async with app.ctx.asyncsession as session:
        async with session.begin():
            config_dal = ConfigDAL(session)
            config = await config_dal.get(key)
            return config.value

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
            
            ## make sure that the datatype of the value is the same as the one in the database
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

            await config_dal.update(key, value)

async def init_config(app):
    """
    Initialize the configuration of the application.
    """
    async with app.ctx.asyncsession as session:
        async with session.begin():
            config_dal = ConfigDAL(session)

            for config_value in CONFIG_VALUES:
                if not await config_dal.get_by_name(config_value[0]):
                    await config_dal.new(config_value[0], config_value[1], config_value[2], config_value[3])
    
    app.ctx.config = type('', (), {})()
    app.ctx.config.get = get_config_value
    app.ctx.config.update = update_config_value