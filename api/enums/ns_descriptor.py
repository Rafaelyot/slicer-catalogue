from api.enums.utils import AutoName
from enum import auto


class LayerProtocol(AutoName):
    ETHERNET = auto()
    MPLS = auto()
    ODU2 = auto()
    IPV4 = auto()
    IPV6 = auto()
    PSEUDO_WIRE = auto()

    # Extended for optical
    OTSIA = auto()
    OCH = auto()
    OTU = auto()
    ODU = auto()
    SDM = auto()
    AROF = auto()

    # To handle old cases
    NOT_SPECIFIED = auto()


class CpRole(AutoName):
    ROOT = auto()
    LEAF = auto()


class AddressType(AutoName):
    MAC_ADDRESS = auto()
    IP_ADDRESS = auto()


class IpVersion(AutoName):
    IPv4 = auto()
    IPv6 = auto()


class ServiceAvailabilityLevel(AutoName):
    LEVEL_1 = auto()
    LEVEL_2 = auto()
    LEVEL_3 = auto()


class NsScaleType(AutoName):
    SCALE_NS = auto()
    SCALE_VNF = auto()


class LcmEventType(AutoName):
    # VNF lifecycle event
    START_VNF_INSTANTIATION = auto()
    END_VNF_INSTANTIATION = auto()
    START_VNF_SCALING = auto()
    END_VNF_SCALING = auto()
    START_VNF_HEALING = auto()
    END_VNF_HEALING = auto()
    START_VNF_TERMINATION = auto()
    END_VNF_TERMINATION = auto()
    START_VNF_FLAVOUR_CHANGE = auto()
    END_VNF_FLAVOUR_CHANGE = auto()
    START_VNF_OP_STATE_CHANGE = auto()
    END_VNF_OP_STATE_CHANGE = auto()
    START_CHANGE_VNF_EXTERNAL_CONNECTIVITY = auto()
    END_CHANGE_VNF_EXTERNAL_CONNECTIVITY = auto()

    # external trigger detected on a VNFM reference point
    RECEIVED_MSG_VNF_INSTANTIATE = auto()
    RECEIVED_MSG_VNF_SCALE = auto()
    RECEIVED_MSG_VNF_HEAL = auto()
    RECEIVED_MSG_VNF_TERMINATE = auto()
    RECEIVED_MSG_CHANGE_VNF_FLAVOUR = auto()
    RECEIVED_MSG_CHANGE_VNF_EXTERNAL_CONNECTIVITY = auto()
    RECEIVED_MSG_CHANGE_VNF_OP_STATE = auto()
    RECEIVED_MSG_VNF_CHANGE_INDICATION = auto()

    # NS lifecycle event
    START_NS_INSTANTIATION = auto()
    END_NS_INSTANTIATION = auto()
    START_NS_SCALING = auto()
    END_NS_SCALING = auto()
    START_NS_HEALING = auto()
    END_NS_HEALING = auto()
    START_NS_TERMINATION = auto()
    END_NS_TERMINATION = auto()
    START_NS_UPDATE = auto()
    END_NS_UPDATE = auto()

    # external trigger
    RECEIVED_MSG_NS_INSTANTIATE = auto()
    RECEIVED_MSG_NS_SCALE = auto()
    RECEIVED_MSG_NS_HEAL = auto()
    RECEIVED_MSG_NS_TERMINATE = auto()
    RECEIVED_MSG_NS_UPDATE = auto()


class AffinityType(AutoName):
    AFFINITY = auto()
    ANTI_AFFINITY = auto()


class AffinityScope(AutoName):
    NFVI_NODE = auto()
    NFVI_POP = auto()
    ZONE = auto()
    ZONE_GROUP = auto()


class ScalingProcedureType(AutoName):
    MANUAL_SCALING = auto()
    AUTOMATED_SCALING = auto()


class LogicOperation(AutoName):
    AND = auto()
    OR = auto()


class RelationalOperation(AutoName):
    GE = auto()
    LE = auto()
    GT = auto()
    LT = auto()
    EQ = auto()
