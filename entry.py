from sanic import Sanic
from blueprints import blueprints
from core.env_manager import EnvManager
from core.server_events import before_server_start, after_server_start, before_server_stop

env_manager = EnvManager()

app = Sanic(env_manager.get("APP_NAME"))

app.ctx.env_manager = env_manager

app.before_server_start(before_server_start, priority=0)
app.after_server_start(after_server_start, priority=0)
app.before_server_stop(before_server_stop, priority=0)

for blueprint in blueprints:
    if blueprint.version in env_manager.get("ACTIVE_VERSIONS"):
        app.blueprint(blueprint)

if __name__ == "__main__":
    app.run(host=env_manager.get("APP_HOST"), port=env_manager.get("APP_PORT"), auto_reload=env_manager.get("RELOAD_MODE"), debug=env_manager.get("DEBUG_MODE"), dev=env_manager.get("DEV_MODE"))