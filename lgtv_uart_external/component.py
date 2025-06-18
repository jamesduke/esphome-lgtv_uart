import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import binary_sensor, uart
from esphome.const import CONF_ID, CONF_NAME, CONF_UART_ID

# Declare the C++ namespace if your component uses one.
# If LGTVUARTComponent is in the global namespace, this line can be omitted
# or adjusted. For simplicity, assuming global or a specific namespace.
# For this example, let's assume LGTVUARTComponent is in the global namespace
# or the header handles its namespace context correctly.
# lgtv_uart_ns = cg.global_ns.namespace('lgtv_uart_ns')
# LGTVUARTComponent = lgtv_uart_ns.class_('LGTVUARTComponent', cg.Component, uart.UARTDevice, binary_sensor.BinarySensor)
# Simpler approach if no explicit namespace is defined in the .h for the class itself:
LGTVUARTComponent = cg.global_ns.class_('LGTVUARTComponent', cg.Component, uart.UARTDevice, binary_sensor.BinarySensor)


# Define the platform name that will be used in the YAML
# e.g., binary_sensor: - platform: lgtv_uart
# For clarity, let's name it 'lgtv_uart_custom_binary_sensor' to avoid potential
# conflicts if there was ever an official 'lgtv_uart' component.
# Or more simply, just 'lgtv_uart_external' to match directory. Let's use this.
PLATFORM_SCHEMA = binary_sensor.BINARY_SENSOR_SCHEMA.extend({
    cv.GenerateID(): cv.declare_id(LGTVUARTComponent),
    cv.Required(CONF_UART_ID): cv.use_id(uart.UARTComponent),
    # CONF_NAME is usually handled by BINARY_SENSOR_SCHEMA
}).extend(cv.COMPONENT_SCHEMA) # Include component essentials like update_interval

async def to_code(config):
    # Get the UART parent
    parent = await cg.get_variable(config[CONF_UART_ID])

    # Create an instance of the LGTVUARTComponent
    var = cg.new_Pvariable(config[CONF_ID], parent) # Pass uart_parent to constructor

    # Register it as a component
    await cg.register_component(var, config)

    # Register it as a binary_sensor
    await binary_sensor.register_binary_sensor(var, config)

    # If LGTVUARTComponent.h is in the same directory as component.py,
    # ESPHome should pick it up automatically.
    # If it's in a subdirectory, e.g., 'includes', you might need:
    # cg.add_library('','','local_path_to_includes_dir_if_any')
    # cg.add_global_includes('lgtv_uart.h') # Or specific path if not auto-detected

    # For this setup, where lgtv_uart.h is in the same dir (lgtv_uart_external),
    # ESPHome's build system usually adds this directory to include paths.
    # Explicitly adding the header can ensure it's found.
    cg.add_global_includes('lgtv_uart.h')
