from bson import ObjectId
from api.models.vs_blueprint import VsBlueprintInfo, VsBlueprint, VsdNsdTranslationRule
from api.models.ns_template import Nst
from api.exceptions.exceptions import MalFormedException, FailedOperationException, AlreadyExistingEntityException
from api.exceptions.utils import exception_message_elements
from mongoengine.queryset.visitor import Q
from api.queries.utils import transaction
from api.queries.vs_descriptor import get_vs_descriptors
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
def get_vs_blueprints(vsb_id=None, vsb_name=None, vsb_version=None, tenant_id=None, with_translation_rules=False):
    arguments = locals()
    arguments.pop('with_translation_rules', None)
    parameters_size = len(dict(filter(lambda a: a[-1] is not None, arguments.items())))

    if parameters_size == 1 and (vsb_id is not None):
        vsbi = VsBlueprintInfo.get_or_404(vs_blueprint_id=vsb_id)
        vsbi.vs_blueprint = VsBlueprint.get_or_404(blueprint_id=vsb_id)
        if with_translation_rules:
            vsbi.vs_blueprint.translation_rules = VsdNsdTranslationRule.objects.filter(blueprint_id=vsb_id)

        return [vsbi]

    elif parameters_size == 1 and (tenant_id is not None):
        vsbi_list = []

        for vsbi in VsBlueprintInfo.objects.all():
            vsbi.vs_blueprint = VsBlueprint.get_or_404(name=vsbi.name, version=vsbi.vs_blueprint_version)
            if with_translation_rules:
                vs_blueprint_id = vsbi.vs_blueprint.blueprint_id
                vsbi.vs_blueprint.translation_rules = VsdNsdTranslationRule.objects.filter(blueprint_id=vs_blueprint_id)
            vsbi_list.append(_post_process_vsb(vsbi, tenant_id))

        return vsbi_list

    elif parameters_size == 2 and (vsb_name is not None) and (vsb_version is not None):
        vsbi = VsBlueprintInfo.get_or_404(name=vsb_name, vs_blueprint_version=vsb_version)
        vsbi.vs_blueprint = VsBlueprint.get_or_404(name=vsb_name, version=vsb_version)
        if with_translation_rules:
            vs_blueprint_id = vsbi.vs_blueprint.blueprint_id
            vsbi.vs_blueprint.translation_rules = VsdNsdTranslationRule.objects.filter(blueprint_id=vs_blueprint_id)

        return [vsbi]

    elif parameters_size == 2 and (vsb_id is not None) and (tenant_id is not None):
        vsbi = VsBlueprintInfo.get_or_404(vs_blueprint_id=vsb_id)
        vsbi.vs_blueprint = VsBlueprint.get_or_404(blueprint_id=vsb_id)
        if with_translation_rules:
            vsbi.vs_blueprint.translation_rules = VsdNsdTranslationRule.get_or_404(blueprint_id=vsb_id)

        return [_post_process_vsb(vsbi, tenant_id)]

    elif parameters_size == 0:
        all_vsbi = VsBlueprintInfo.objects.all()
        for vsbi in all_vsbi:
            vsbi.vs_blueprint = VsBlueprint.get_or_404(name=vsbi.name, version=vsbi.vs_blueprint_version)
            if with_translation_rules:
                vs_blueprint_id = vsbi.vs_blueprint.blueprint_id
                vsbi.vs_blueprint.translation_rules = VsdNsdTranslationRule.get_or_404(blueprint_id=vs_blueprint_id)

        return all_vsbi

    raise MalFormedException()


def delete_vs_blueprint(vsb_id):
    vsbi = VsBlueprintInfo.get_or_404(vs_blueprint_id=vsb_id)
    if len(vsbi.active_vsd_id) > 0:
        raise FailedOperationException("There are some VSDs associated to the VS Blueprint. Impossible to remove it.")

    def delete_callback(session):
        VsBlueprintInfo._get_collection().delete_one({
            "vs_blueprint_id": vsb_id
        }, session=session)

        VsBlueprint._get_collection().delete_one({
            "blueprint_id": vsb_id
        }, session=session)

    transaction(delete_callback)


def _onboard_vnf_package(vnf):
    pass


def _on_board_ns_template(data):
    """
    version, target_name, target_id = nst.get('nst_version'), nst.get('nst_name'), nst.get('nst_id')

    if Nst.objects.filter((Q(nst_name=target_name) & Q(nst_version=version)) | Q(nst_id=target_id)).count() > 0:
        raise AlreadyExistingEntityException(f"NsTemplate with name {target_name} and version {version} or ID exists")
    """
    nsts, nsds, vnf_packages = data.get('nsts', []), data.get('nsds', []), data.get('vnf_packages', [])

    for vnf in vnf_packages:
        pass


def _process_ns_descriptor_onboarding(data):
    nsts, nsds, vnf_packages = data.get('nsts', []), data.get('nsds', []), data.get('vnf_packages', [])

    if len(nsts) == 0 and len(nsds) == 0 and len(vnf_packages) == 0:
        return

    if len(nsts) > 0:
        pass

    if len(vnf_packages) > 0:
        # TODO: Implement vnf_packages logic
        pass

    if len(nsds) > 0:
        # TODO: Implement nsds logic
        pass

    for nst in nsts:
        nst_name, version, nst_id = nst.nst_name, nst.nst_version, nst.nst_id
        if Nst.objects.filter(nst_name=nst_name, version=version).count() > 0 or \
                Nst.objects.filter(nst_id=nst_id).count() > 0:
            raise AlreadyExistingEntityException(f"NsTemplate with name {nst_name} and version {version} or ID exists")

    def create_callback(session):
        Nst._get_collection().insert_many(nsts, session=session)

    transaction(create_callback)


def create_vs_blueprint(data):
    _process_ns_descriptor_onboarding(data)

    """
    vs_blueprint = data.get('vs_blueprint', {})

    name, version, owner = vs_blueprint.get('name'), vs_blueprint.get('version'), data.get('owner')

    if VsBlueprintInfo.objects.filter(name=name, vs_blueprint_version=version).count() > 0 or \
            VsBlueprint.objects.filter(name=name, version=version).count() > 0:
        class_name, args = exception_message_elements(VsBlueprint, name=name, version=version)

        raise AlreadyExistingEntityException(f"{class_name} with {args} already present in DB")

    _id = ObjectId()
    data['_id'] = _id
    vs_blueprint_id = vs_blueprint['blueprint_id'] = str(_id)

    translation_rules = data.get('translation_rules', [])
    for translation_rule in translation_rules:
        translation_rule.blueprint_id = vs_blueprint_id

    def create_callback(session):
        VsBlueprint.get_collection().insert_one(data, session=session)
        VsBlueprintInfo.get_collection().insert_one({
            'vs_blueprint_id': vs_blueprint_id,
            'vs_blueprint_version': version,
            'name': name,
            'owner': owner
        }, session=session)
        VsdNsdTranslationRule.get_collection().insert_many(translation_rules, session=session)

    transaction(create_callback)

    return vs_blueprint_id
    """
