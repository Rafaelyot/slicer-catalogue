from flask import Blueprint, jsonify
from auth import is_authenticated
from serializers.vsblueprint import VsBlueprintInfoSerializer
from queries.vsblueprint import query_vs_blueprint
from http import HTTPStatus

# noinspection PyRedeclaration
app = Blueprint('vsblueprint', __name__)


@app.route('/vsblueprint', methods=('GET',))
def get_blueprints(id=None, site=None):
    if not is_authenticated():
        return False

    serializer = VsBlueprintInfoSerializer(query_vs_blueprint(vsb_version='version_0', vsb_name='name_0'), many=True)

    return jsonify(serializer.data), HTTPStatus.OK
