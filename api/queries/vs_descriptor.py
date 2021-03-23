from bson import ObjectId

from enums.vs_blueprint import VsComponentType
from exceptions.exceptions import MalFormedException, AlreadyExistingEntityException
from models.vs_descriptor import VsDescriptor
from models.vs_blueprint import VsBlueprintInfo, VsBlueprint
from queries.utils import transaction
from exceptions.exceptions import FailedOperationException


def get_vs_descriptors(tenant_id=None, vsd_id=None):
    arguments = locals()
    parameters_size = len(dict(filter(lambda a: a[-1] is not None, arguments.items())))

    if parameters_size == 1 and (tenant_id is not None):
        if False:  # is_admin(tenant_id)
            return VsDescriptor.objects.all()

        else:
            vs_descriptors = VsDescriptor.objects.filter(tenant_id=tenant_id)

            for vsd in VsDescriptor.objects.filter(is_public=True):
                if vsd.tenant_id == tenant_id and vsd not in vs_descriptors:
                    vs_descriptors.append(vsd)

            return vs_descriptors

    elif parameters_size == 2 and (tenant_id is not None) and (vsd_id is not None):
        if False:  # is_admin(tenant_id)
            return [VsDescriptor.get_or_404(descriptor_id=vsd_id)]
        else:
            return [VsDescriptor.get_or_404(descriptor_id=vsd_id, tenant_id=tenant_id)]

    elif parameters_size == 0:
        return VsDescriptor.objects.filter(is_public=True)

    raise MalFormedException()


def delete_vs_descriptor(tenant_id, vsd_id):
    vsd = VsDescriptor.get_or_404(descriptor_id=vsd_id, tenant_id=tenant_id)
    active_vsd_id = list(VsBlueprintInfo.get_or_404(vs_blueprint_id=vsd.vs_blueprint_id).active_vsd_id)
    is_admin = False

    if vsd.tenant_id == tenant_id or is_admin:
        def delete_callback(session):
            VsDescriptor._collection.delete_one({
                "descriptor_id": vsd_id
            }, session=session)

            if vsd_id in active_vsd_id:
                active_vsd_id.remove(vsd_id)

            query = {"vs_blueprint_id": vsd.vs_blueprint_id}
            updated_values = {"$set": {"active_vsd_id": active_vsd_id}}
            VsBlueprintInfo._collection.update_one(query, updated_values, session=session)

        transaction(delete_callback)

    else:
        raise FailedOperationException(f"Tenant {tenant_id} does not have the right to remove the VSD {vsd_id}")


def _store_vsd(data):
    name, version, tenant_id = data.get('name'), data.get('version'), data.get('tenant_id')

    if VsDescriptor.objects.filter(name=name, version=version, tenant_id=tenant_id).count() > 0:
        raise AlreadyExistingEntityException(
            f"VSD with name {name} and version {version} for tenant {tenant_id} already present")

    _id = ObjectId()
    data['_id'] = _id
    data['descriptor_id'] = vs_descriptor_id = str(_id)

    def create_callback(session):
        VsDescriptor._collection.insert_one(data, session=session)

    transaction(create_callback)

    return vs_descriptor_id


def _onboard_nested_vsd(component, data):
    name = f"{data.get('name')}_{component.component_id}"
    nested_vsd_qos_params = list(filter(lambda param_id: param_id.startswith(f"{component.component_id}."),
                                        data.get('qos_parameters').keys()))

    qos_params = {}
    for param in nested_vsd_qos_params:
        nested_id = param.replace(f"{component.component_id}.", "")
        qos_params[nested_id] = data.get('qos_parameters').get(param)

    data['name'] = name
    data['vs_blueprint_id'] = component.associated_vsb_id
    data['qos_parameters'] = qos_params

    if component.compatible_site is None:
        return create_vs_descriptor(data)

    else:
        data['domain_id'] = component.compatible_site
        return _store_vsd(data)


def create_vs_descriptor(data):
    vs_blueprint_id, tenant_id, nested_vsd_ids = data.get('vs_blueprint_id'), data.get('tenant_id'), data.get(
        'nested_vsd_ids')
    vs_blueprint = VsBlueprint.get_or_404(blueprint_id=vs_blueprint_id)

    nested_vsd_ids = {}
    for component in vs_blueprint.atomic_components:
        if component.type == VsComponentType.SERVICE.value and component.component_id not in nested_vsd_ids:
            nested_vsd_ids[component.component_id] = _onboard_nested_vsd(component, data)

    nested_vsd_ids.update(data.get('nested_vsd_ids', {}))

    data['nested_vsd_ids'] = nested_vsd_ids
    vs_descriptor_id = _store_vsd(data)

    vs_blueprint_info = VsBlueprintInfo.get_or_404(vs_blueprint_id=vs_blueprint_id)
    active_vsd_id = list(vs_blueprint_info.active_vsd_id)

    def create_callback(session):
        query = {"vs_blueprint_id": vs_blueprint_info.vs_blueprint_id}
        active_vsd_id.append(vs_descriptor_id)
        updated_values = {"$set": {"active_vsd_id": active_vsd_id}}
        VsBlueprintInfo._collection.update_one(query, updated_values, session=session)

    transaction(create_callback)

    return vs_descriptor_id