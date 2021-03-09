import queries.vs_blueprint
from flask import Blueprint, request
from http import HTTPStatus
from serializers.vsblueprint import VsBlueprintInfoSerializer
from views.utils import response_template
from exceptions.utils import handle_exception

# noinspection PyRedeclaration
app = Blueprint('vsblueprint', __name__)


@handle_exception(app)
@app.route('/vsblueprint', methods=('GET',))
def get_vs_blueprints():
    tenant_id = None  # TODO: tenant_id it is obtained from the authenticated user (authentication not yet implemented)
    args = {
        'tenant_id': tenant_id,
        'vsb_id': request.args.get('vsb_id'),
        'vsb_name': request.args.get('vsb_name'),
        'vsb_version': request.args.get('vsb_version'),
    }

    serializer = VsBlueprintInfoSerializer(queries.vs_blueprint.get_vs_blueprints(**args), many=True)

    return response_template('Success', serializer.data)


@handle_exception(app)
@app.route('/vsblueprint', methods=('DELETE',))
def delete_vs_blueprint():
    vsb_id = request.args.get('vsb_id')

    queries.vs_blueprint.delete_vs_blueprint(vsb_id)

    return response_template('Success', status_code=HTTPStatus.NO_CONTENT)
