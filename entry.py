from sanic import Sanic
from blueprints import blueprints

app = Sanic("")

for blueprint in blueprints:
    if blueprint.version in ["v0"]:
        app.blueprint(blueprint)

if __name__ == "__main__":
    app.run(host="", port=8000, auto_reload=False, debug=False, dev=False)