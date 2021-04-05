from flask import Blueprint, request
from marshmallow import ValidationError
from http import HTTPStatus
from api.exceptions.utils import handle_exception
from api.serializers.vs_descriptor import VsDescriptorSerializer
from api.views.utils import response_template
from api.exceptions.exceptions import BadVsBlueprintBody
import api.queries.vs_descriptor as queries

app = Blueprint('vsdescriptor', __name__)

handle_exception(app)  # Handle errors


@app.route("/vsdescriptor", methods=('GET',))
def get_vs_descriptors():
    # TODO: tenant_id it is obtained from the authenticated user (authentication not yet implemented)
    args = {
        'tenant_id': request.args.get('tenant_id'),  # <-CHANGE THIS->,
        'vsd_id': request.args.get('vsd_id')
    }

    serializer = VsDescriptorSerializer(many=True)
    data = serializer.dump(queries.get_vs_descriptors(**args))

    return response_template('Success', data)


@app.route('/vsdescriptor', methods=('DELETE',))
def delete_vs_descriptor():
    # TODO: tenant_id it is obtained from the authenticated user (authentication not yet implemented)
    args = {
        'tenant_id': request.args.get('tenant_id'),  # <-CHANGE THIS->
        'vsd_id': request.args.get('vsd_id')
    }

    queries.delete_vs_descriptor(**args)
    return response_template('Success', status_code=HTTPStatus.NO_CONTENT)


@app.route('/vsdescriptor', methods=('POST',))
def create_vs_descriptor():
    request_data = request.get_json()

    serializer = VsDescriptorSerializer()
    try:
        validated_data = serializer.load(request_data)
    except ValidationError as error:
        raise BadVsBlueprintBody(error.messages)

    vs_descriptor_id = queries.create_vs_descriptor(validated_data)
    return response_template('Success', data={'vs_descriptor_id': vs_descriptor_id}, status_code=HTTPStatus.CREATED)
