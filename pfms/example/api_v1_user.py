from flask import Blueprint
from pfms.swagger.pfms_swagger_decorator import request_response
from pfms.example.dto.details import Details

user_blueprint = Blueprint('user_blueprint', __name__, url_prefix="/api/v1/user")


@user_blueprint.route("/create", methods=["POST", "GET"])
@request_response(request_body=Details, response_obj=Details)
def create():
    return "Created"


@user_blueprint.route("/details/<int:id>", methods=["GET"])
@request_response(request_body=Details, response_obj=Details)
def details(id):
    return "Response " + str(id)


@user_blueprint.route("/", methods=["GET"])
@request_response(request_body=Details, response_obj=Details)
def bismillah():
    return "Response "

# @user_blueprint.route("/update", methods=["POST"])
# def update():
#     pass
#



#
# @user_blueprint.route("/list", methods=["GET"])
# def list():
#     pass
#
# @user_blueprint.route("/delete/<int:id>", methods=["DELETE"])
# def delete(id):
#     pass
#
# @user_blueprint.route("/bulk-create", methods=["POST"])
# def bulk_create():
#     pass
#
#
# @user_blueprint.route("/bulk-update", methods=["POST"])
# def bulk_update():
#     pass
#
#
# @user_blueprint.route("/bulk-delete", methods=["DELETE"])
# def bulk_delete():
#     pass