import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import binary_sensor, uart
from esphome.const import CONF_ID

# Assuming the C++ class is within the esphome::lgtv_uart namespace
lgtv_uart_ns = cg.esphome_ns.namespace("lgtv_uart")
LGTVUARTComponent = lgtv_uart_ns.class_("LGTVUARTComponent", binary_sensor.BinarySensor, cg.Component, uart.UARTDevice)

CONFIG_SCHEMA = (
    binary_sensor.binary_sensor_schema(LGTVUARTComponent)
    .extend(uart.uart_device_schema)
)

async def to_code(config):
    # Get the UART parent variable
    uart_device = await cg.get_variable(config[uart.CONF_UART_ID])
    
    # Create the LGTVUARTComponent variable, passing the uart_device to the constructor
    var = cg.new_Pvariable(config[CONF_ID], uart_device)

    # Register the component and binary sensor
    await cg.register_component(var, config)
    await binary_sensor.register_binary_sensor(var, config)
