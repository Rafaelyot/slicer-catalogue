from models.vsblueprint import VsBlueprintInfo, VsBlueprint


# noinspection PyTypeChecker
def query_vs_blueprint(vsb_id=None, vsb_name=None, vsb_version=None, tenant_id=None):
    arguments = locals()
    parameters_size = len(dict(filter(lambda a: a is not None, arguments.items())))

    if parameters_size == 1 and (vsb_id is not None):
        vsbi = VsBlueprintInfo.objects.get(vs_blueprint_id=vsb_id)
        vsbi.vs_blueprint = VsBlueprint.objects.get(blueprint_id=vsb_id)
        return [vsbi]

    elif parameters_size == 1 and tenant_id is not None:
        return []

    elif parameters_size == 2 and (vsb_name is not None) and (vsb_version is not None):
        vsbi = VsBlueprintInfo.objects.get(name=vsb_name, vs_blueprint_version=vsb_version)
        vsbi.vs_blueprint = VsBlueprint.objects.get(name=vsb_name, version=vsb_version)
        return [vsbi]

    elif parameters_size == 2 and (vsb_id is not None) and (tenant_id is not None):
        # TODO: Implement this later (It is related to vs_descriptor which is not implemented yet)
        return []

    elif parameters_size == 0:
        return []

    else:
        return []
