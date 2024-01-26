"""Quirk for smarthjemmet.dk QUAD-ZIG-SW."""

from zigpy.profiles import zha 
from zigpy.quirks import CustomDevice
from zigpy.zcl.clusters.general import (
    Basic,
    MultistateInput,
    OnOffConfiguration,
    PowerConfiguration,
)
from zhaquirks.const import (
    DEVICE_TYPE,
    ENDPOINTS,
    INPUT_CLUSTERS,
    MODELS_INFO,
    OUTPUT_CLUSTERS,
    PROFILE_ID,
)


class SmarthjemmetDkQuadZigSw(CustomDevice):
    """Smarthjemmet.Dk QUAD-ZIG-SW custom device implementation."""

    signature = {
        MODELS_INFO: [("smarthjemmet.dk", "QUAD-ZIG-SW")],
        ENDPOINTS: {
            1: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.ON_OFF_SWITCH,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    PowerConfiguration.cluster_id,
                    OnOffConfiguration.cluster_id,
                ],
                OUTPUT_CLUSTERS: [
                    Basic.cluster_id,
                    PowerConfiguration.cluster_id,
                    MultistateInput.cluster_id,
                ],
            },
            2: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.ON_OFF_SWITCH,
                INPUT_CLUSTERS: [
                    OnOffConfiguration.cluster_id,
                ],
                OUTPUT_CLUSTERS: [
                    MultistateInput.cluster_id,
                ],
            },
            3: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.ON_OFF_SWITCH,
                INPUT_CLUSTERS: [
                    OnOffConfiguration.cluster_id,
                ],
                OUTPUT_CLUSTERS: [
                    MultistateInput.cluster_id,
                ],
            },
            4: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.ON_OFF_SWITCH,
                INPUT_CLUSTERS: [
                    OnOffConfiguration.cluster_id,
                ],
                OUTPUT_CLUSTERS: [
                    MultistateInput.cluster_id,
                ],
            },
            5: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.ON_OFF_SWITCH,
                INPUT_CLUSTERS: [
                    OnOffConfiguration.cluster_id,
                ],
                OUTPUT_CLUSTERS: [
                    MultistateInput.cluster_id,
                ],
            },
        },
    }

    replacement = {
        ENDPOINTS: {
            1: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.ON_OFF_SWITCH,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    PowerConfiguration.cluster_id,
                    OnOffConfiguration.cluster_id,
                ],
                OUTPUT_CLUSTERS: [
                    Basic.cluster_id,
                    PowerConfiguration.cluster_id,
                    MultistateInput.cluster_id,
                ],
            },
            2: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.ON_OFF_SWITCH,
                INPUT_CLUSTERS: [
                    OnOffConfiguration.cluster_id,
                ],
                OUTPUT_CLUSTERS: [
                    MultistateInput.cluster_id,
                ],
            },
            3: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.ON_OFF_SWITCH,
                INPUT_CLUSTERS: [
                    OnOffConfiguration.cluster_id,
                ],
                OUTPUT_CLUSTERS: [
                    MultistateInput.cluster_id,
                ],
            },
            4: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.ON_OFF_SWITCH,
                INPUT_CLUSTERS: [
                    OnOffConfiguration.cluster_id,
                ],
                OUTPUT_CLUSTERS: [
                    MultistateInput.cluster_id,
                ],
            },
            5: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.ON_OFF_SWITCH,
                INPUT_CLUSTERS: [
                    OnOffConfiguration.cluster_id,
                ],
                OUTPUT_CLUSTERS: [
                    MultistateInput.cluster_id,
                ],
            },
        },
    }
