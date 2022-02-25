import esphome.codegen as cg
import esphome.config_validation as cv
from esphome import core, pins
from esphome.components import modbus
from esphome.const import CONF_ID

infoPanel_ns = cg.esphome_ns.namespace('infopanel')
InfoPanel = infoPanel_ns.class_('InfoPanel', cg.PollingComponent)

CONF_INFOPANEL_ID = 'infoPanel_id'

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(InfoPanel),
}).extend(cv.polling_component_schema('60s'))

def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    yield cg.register_component(var, config)