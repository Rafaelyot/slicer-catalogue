from models.vs_blueprint import VsBlueprintInfo, VsBlueprint
from exceptions.vs_blueprint import MalFormedException


# noinspection PyTypeChecker
def query_vs_blueprint(vsb_id=None, vsb_name=None, vsb_version=None, tenant_id=None):
    arguments = locals()
    parameters_size = len(dict(filter(lambda a: a[-1] is not None, arguments.items())))

    if parameters_size == 1 and (vsb_id is not None):
        vsbi = VsBlueprintInfo.get_or_404(vs_blueprint_id=vsb_id)
        vsbi.vs_blueprint = VsBlueprint.get_or_404(blueprint_id=vsb_id)
        return [vsbi]

    elif parameters_size == 1 and (tenant_id is not None):
        # TODO: Implement this later (It is related to vs_descriptor which is not implemented yet)
        return []

    elif parameters_size == 2 and (vsb_name is not None) and (vsb_version is not None):
        vsbi = VsBlueprintInfo.get_or_404(name=vsb_name, vs_blueprint_version=vsb_version)
        vsbi.vs_blueprint = VsBlueprint.get_or_404(name=vsb_name, version=vsb_version)
        return [vsbi]

    elif parameters_size == 2 and (vsb_id is not None) and (tenant_id is not None):
        # TODO: Implement this later (It is related to vs_descriptor which is not implemented yet)
        return []

    elif parameters_size == 0:
        all_vsbi = VsBlueprintInfo.objects.all()
        for vsbi in all_vsbi:
            vsbi.vs_blueprint = VsBlueprint.get_or_404(name=vsbi.name, version=vsbi.vs_blueprint_version)

        return all_vsbi

    raise MalFormedException()
