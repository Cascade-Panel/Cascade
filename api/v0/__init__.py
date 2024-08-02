""" This module is responsible for creating the blueprint for the v0 API. """

from sanic import Blueprint
from api.v0.views import views

v0_bp = Blueprint('Version 0', version_prefix="/api", version="v0")

for view in views:
    v0_bp.add_route(
        handler=view.as_view(), 
        uri=view.uri
    )