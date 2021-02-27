from flask import Blueprint, request
from pfms.common.pfms_data_type import string, number
from pfms.pfapi.rr.pfms_request_respons import PfRequestResponse
from pfms.swagger.pfms_swagger_decorator import request_response, create, request_response_list, simple_get, bulk_create
from pfms.example.dto.details import Details

user_blueprint = Blueprint('user_blueprint', __name__, url_prefix="/api/v1/user")
rr = PfRequestResponse()


@user_blueprint.route("/create", methods=["POST"])
@create(request_body=Details, response_obj=Details)
def create():
    details = rr.json_request_process(Details())
    data_list = ["1.2"]
    return rr.bulk_data_response(data_list)


@user_blueprint.route("/details/<int:id>/<string:name>", methods=["POST"])
@bulk_create(request_body=Details, response_obj=Details)
def details(id, name):
    return "Response " + str(id)


@user_blueprint.route("/", methods=["GET"])
@request_response_list(request_body=Details, response_obj=Details)
def bismillah():
    return "Response "


@user_blueprint.route("/simple-get", methods=["GET"])
@simple_get(query_param=[("name", string), ("age", number)], response_obj=Details)
def simple_get():
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