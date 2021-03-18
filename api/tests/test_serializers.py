"""
Test serializers' validators
"""
from tests.utils import catch_exception, error_catcher, mixer
from serializers.vs_blueprint import VsdNsdTranslationRuleSerializer, VsdParameterValueRangeSerializer


def generate_data(cls, remove_fields=None):
    if remove_fields is None:
        remove_fields = []

    data = {}
    for _ in range(10):  # Retry blending, because it is very unstable (sometimes it is returning None)
        data = mixer.blend(cls)
        if data:
            break

    for field in remove_fields:
        data.pop(field, None)

    return data


# VsdParameterValueRangeSerializer
@catch_exception
def test_vsd_parameter_value_range_serializer_invalid_parameter_id(error_catcher):
    field = "parameter_id"
    data = generate_data(VsdParameterValueRangeSerializer, remove_fields=[field])
    errors = VsdParameterValueRangeSerializer().validate(data)
    assert len(errors) > 0 and errors.get(field)[0] == "VSD parameter value range without ID."


# VsdNsdTranslationRuleSerializer
@catch_exception
def test_vsd_nsd_translation_rule_serializer_invalid_input_none(error_catcher):
    field = "input"
    data = generate_data(VsdNsdTranslationRuleSerializer, remove_fields=[field])
    errors = VsdNsdTranslationRuleSerializer().validate(data)
    assert len(errors) > 0 and errors.get(field)[0] == "VSD NSD translation rule without matching conditions"


@catch_exception
def test_vsd_nsd_translation_rule_serializer_invalid_input_empty(error_catcher):
    field = "input"
    data = generate_data(VsdNsdTranslationRuleSerializer)
    data[field] = []
    errors = VsdNsdTranslationRuleSerializer().validate(data)
    assert len(errors) > 0 and errors.get(field)[0] == "VSD NSD translation rule without matching conditions"


@catch_exception
def test_vsd_nsd_translation_rule_serializer_invalid_nst_id_and_nsd_id(error_catcher):
    fields = ["nst_id", "nsd_id"]
    data = generate_data(VsdNsdTranslationRuleSerializer, remove_fields=fields)
    errors = VsdNsdTranslationRuleSerializer().validate(data)
    assert len(errors) > 0 and errors.get(" & ".join(fields))[0] == "VSD NSD translation rule without NSD ID/NST ID"


@catch_exception
def test_vsd_nsd_translation_rule_serializer_invalid_nsd_id_and_nsd_version(error_catcher):
    field = "nsd_version"
    data = generate_data(VsdNsdTranslationRuleSerializer, remove_fields=[field])
    errors = VsdNsdTranslationRuleSerializer().validate(data)
    assert len(errors) > 0 and errors.get(f'nsd_id & {field}')[0] == "VSD NSD translation rule without NSD version"
