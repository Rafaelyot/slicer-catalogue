import queries.vs_blueprint
from flask import Blueprint, request
from http import HTTPStatus
from marshmallow import ValidationError
from serializers.vs_blueprint import VsBlueprintInfoSerializer
from serializers.requests import VsBlueprintRequestSerializer
from views.utils import response_template
from exceptions.utils import handle_exception
from exceptions.vs_blueprint import BadVsBlueprintBody

# noinspection PyRedeclaration
app = Blueprint('vsblueprint', __name__)

handle_exception(app)  # Handle errors


@app.route('/vsblueprint', methods=('GET',))
def get_vs_blueprints():
    tenant_id = None  # TODO: tenant_id it is obtained from the authenticated user (authentication not yet implemented)
    args = {
        'tenant_id': tenant_id,
        'vsb_id': request.args.get('vsb_id'),
        'vsb_name': request.args.get('vsb_name'),
        'vsb_version': request.args.get('vsb_version'),
    }
    serializer = VsBlueprintInfoSerializer(many=True)
    data = serializer.dump(queries.vs_blueprint.get_vs_blueprints(**args))

    return response_template('Success', data)


@app.route('/vsblueprint', methods=('DELETE',))
def delete_vs_blueprint():
    vsb_id = request.args.get('vsb_id')

    queries.vs_blueprint.delete_vs_blueprint(vsb_id)

    return response_template('Success', status_code=HTTPStatus.NO_CONTENT)


@app.route('/vsblueprint', methods=('POST',))
def create_vs_blueprint():
    # TODO: NST's not implemented yet
    request_data = request.get_json()

    serializer = VsBlueprintRequestSerializer()
    try:
        validated_data = serializer.load(request_data)
    except ValidationError as error:
        raise BadVsBlueprintBody(error.messages)

    # validated_data['owner'] = request_data.get('owner')  # Needed for VsBlueprintInfo
    vs_blueprint_id = queries.vs_blueprint.create_vs_blueprint(validated_data)

    return response_template('Success', data={'vs_blueprint_id': vs_blueprint_id}, status_code=HTTPStatus.CREATED)
