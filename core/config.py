""" A module to manage the configuration of the application. """

from core.database.models.Config import Config
from core.database.DALs.config_dal import ConfigDAL

CONFIG_VALUES = [
   # ['config_name', 'config_type', 'default_value', 'description']
    ['app_name', 'str', 'BlendPanel' 'The name of the application.']
]

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