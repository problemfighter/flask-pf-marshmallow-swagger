from flask import Blueprint

user_blueprint = Blueprint('user_blueprint', __name__, url_prefix="/api/v1/user")


@user_blueprint.route("/simple-response", methods=["GET"])
def simple_response():
    pass