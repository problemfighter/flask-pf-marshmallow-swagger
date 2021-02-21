from flask import Blueprint

user_blueprint = Blueprint('user_blueprint', __name__, url_prefix="/api/v1/user")


@user_blueprint.route("/create", methods=["POST"])
def create():
    pass

@user_blueprint.route("/update", methods=["POST"])
def update():
    pass

@user_blueprint.route("/details/<id:long>", methods=["GET"])
def details():
    pass

@user_blueprint.route("/list", methods=["GET"])
def list():
    pass

@user_blueprint.route("/delete/<id:long>", methods=["DELETE"])
def delete():
    pass

@user_blueprint.route("/bulk-create", methods=["POST"])
def bulk_create():
    pass


@user_blueprint.route("/bulk-update", methods=["POST"])
def bulk_update():
    pass


@user_blueprint.route("/bulk-delete", methods=["DELETE"])
def bulk_delete():
    pass