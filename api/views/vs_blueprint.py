from flask import Blueprint, request
from serializers.vsblueprint import VsBlueprintInfoSerializer
from queries.vs_blueprint import query_vs_blueprint
from views.utils import response_template
from exceptions.utils import handle_exception

# noinspection PyRedeclaration
app = Blueprint('vsblueprint', __name__)


@handle_exception(app)
@app.route('/vsblueprint', methods=('GET',))
def get_blueprints():
    tenant_id = None  # TODO: tenant_id it is obtained from the authenticated user (authentication not yet implemented)
    args = {
        'tenant_id': tenant_id,
        'vsb_id': request.args.get('vsb_id'),
        'vsb_name': request.args.get('vsb_name'),
        'vsb_version': request.args.get('vsb_version'),
    }

    serializer = VsBlueprintInfoSerializer(query_vs_blueprint(**args), many=True)

    return response_template('Success', serializer.data)
