from flask import Blueprint, jsonify
from auth import is_authenticated
from models.vsblueprint import VsBlueprint
from http import HTTPStatus

# noinspection PyRedeclaration
app = Blueprint('vsblueprint', __name__)


@app.route('/vsblueprint', methods=('GET',))
def get_blueprints(id=None, site=None):
    if not is_authenticated():
        return False

    return jsonify(VsBlueprint.objects.all()), HTTPStatus.OK
