import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import binary_sensor, uart
from esphome.const import (
    CONF_ID, # Used for the ID of the binary sensor component
    CONF_UART_ID
    # CONF_NAME will be implicitly handled by BINARY_SENSOR_SCHEMA
)

DEPENDENCIES = ['uart', 'binary_sensor']

# The C++ class that will be our component and binary sensor
LGTVUARTComponent = cg.global_ns.class_('LGTVUARTComponent', cg.Component, uart.UARTDevice, binary_sensor.BinarySensor)

# CONFIG_SCHEMA for the top-level 'lgtv_uart_external:' component.
# It directly includes binary_sensor properties (like name, id) because the component itself IS the binary sensor.
CONFIG_SCHEMA = binary_sensor.BINARY_SENSOR_SCHEMA.extend({
    # cv.GenerateID() is implicitly part of BINARY_SENSOR_SCHEMA for CONF_ID
    # We need to ensure that the ID declared here is for LGTVUARTComponent
    cv.GenerateID(CONF_ID): cv.declare_id(LGTVUARTComponent),
    cv.Required(CONF_UART_ID): cv.use_id(uart.UARTComponent),
}).extend(cv.COMPONENT_SCHEMA) # Also extend COMPONENT_SCHEMA for component lifecycle methods if needed


async def to_code(config):
    # config now holds the data from the top-level 'lgtv_uart_external:' block in YAML

    # Get the UART parent component
    uart_parent = await cg.get_variable(config[CONF_UART_ID])

    # Create an instance of our LGTVUARTComponent.
    # The ID for this instance (var.ID) will come from config[CONF_ID],
    # which is automatically populated by BINARY_SENSOR_SCHEMA.
    var = cg.new_Pvariable(config[CONF_ID], uart_parent)

    # Register this instance as a general ESPHome component
    await cg.register_component(var, config)

    # Register this instance specifically as a binary_sensor.
    # The 'config' dictionary already contains all necessary fields (name, id, etc.)
    # because we extended BINARY_SENSOR_SCHEMA.
    await binary_sensor.register_binary_sensor(var, config)
