from bson import ObjectId
from models.vs_blueprint import VsBlueprintInfo, VsBlueprint
from exceptions.exceptions import MalFormedException, FailedOperationException, AlreadyExistingEntityException
from exceptions.utils import exception_message_elements
from queries.utils import transaction
from queries.vs_descriptor import get_vs_descriptors
from copy import deepcopy


# noinspection PyBroadException
def _post_process_vsb(original_vs_blueprint_info, tenant_id):
    target_vs_blueprint_info = deepcopy(original_vs_blueprint_info)
    target_vs_blueprint_info.active_vsd_id = []

    for id_ in original_vs_blueprint_info.active_vsd_id:
        try:
            target_vs_blueprint_info.active_vsd_id.append(get_vs_descriptors(tenant_id, id_)[0])
        except Exception:
            continue

    return target_vs_blueprint_info


# noinspection PyTypeChecker
def get_vs_blueprints(vsb_id=None, vsb_name=None, vsb_version=None, tenant_id=None):
    arguments = locals()
    parameters_size = len(dict(filter(lambda a: a[-1] is not None, arguments.items())))

    if parameters_size == 1 and (vsb_id is not None):
        vsbi = VsBlueprintInfo.get_or_404(vs_blueprint_id=vsb_id)
        vsbi.vs_blueprint = VsBlueprint.get_or_404(blueprint_id=vsb_id)
        return [vsbi]

    elif parameters_size == 1 and (tenant_id is not None):
        vsbi_list = []

        for vsbi in VsBlueprintInfo.objects.all():
            vsbi.vs_blueprint = VsBlueprint.get_or_404(name=vsbi.name, version=vsbi.vs_blueprint_version)
            vsbi_list.append(_post_process_vsb(vsbi, tenant_id))

        return vsbi_list

    elif parameters_size == 2 and (vsb_name is not None) and (vsb_version is not None):
        vsbi = VsBlueprintInfo.get_or_404(name=vsb_name, vs_blueprint_version=vsb_version)
        vsbi.vs_blueprint = VsBlueprint.get_or_404(name=vsb_name, version=vsb_version)
        return [vsbi]

    elif parameters_size == 2 and (vsb_id is not None) and (tenant_id is not None):
        vsbi = VsBlueprintInfo.get_or_404(vs_blueprint_id=vsb_id)
        vsbi.vs_blueprint = VsBlueprint.get_or_404(blueprint_id=vsb_id)
        return [_post_process_vsb(vsbi, tenant_id)]

    elif parameters_size == 0:
        all_vsbi = VsBlueprintInfo.objects.all()
        for vsbi in all_vsbi:
            vsbi.vs_blueprint = VsBlueprint.get_or_404(name=vsbi.name, version=vsbi.vs_blueprint_version)

        return all_vsbi

    raise MalFormedException()


def delete_vs_blueprint(vsb_id):
    vsbi = VsBlueprintInfo.get_or_404(vs_blueprint_id=vsb_id)
    if len(vsbi.active_vsd_id) > 0:
        raise FailedOperationException("There are some VSDs associated to the VS Blueprint. Impossible to remove it.")

    def delete_callback(session):
        VsBlueprintInfo._collection.delete_one({
            "vs_blueprint_id": vsb_id
        }, session=session)

        VsBlueprint._collection.delete_one({
            "blueprint_id": vsb_id
        }, session=session)

    transaction(delete_callback)


def create_vs_blueprint(data):
    # Todo: Complete this function with NST and NSD
    vs_blueprint = data.get('vs_blueprint', {})

    vs_blueprint.pop('blueprint_id', None)  # blueprint_id it is automatically created
    name, version, owner = vs_blueprint.get('name'), vs_blueprint.get('version'), data.get('owner')

    if VsBlueprintInfo.objects.filter(name=name, vs_blueprint_version=version).count() > 0 or \
            VsBlueprint.objects.filter(name=name, version=version).count() > 0:
        class_name, args = exception_message_elements(VsBlueprint, name=name, version=version)

        raise AlreadyExistingEntityException(f"{class_name} with {args} already present in DB")

    _id = ObjectId()
    data['_id'] = _id
    vs_blueprint_id = vs_blueprint['blueprint_id'] = str(_id)

    def create_callback(session):
        VsBlueprint._collection.insert_one(data, session=session)  # Create and persist VsBlueprint
        VsBlueprintInfo._collection.insert_one({
            'vs_blueprint_id': vs_blueprint_id,
            'vs_blueprint_version': version,
            'name': name,
            'owner': owner
        }, session=session)  # Create and persist VsBlueprintInfo

    transaction(create_callback)

    return vs_blueprint_id
