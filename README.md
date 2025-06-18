# LGTV UART component for ESPHome

ESPHome custom component for DIY LGTV controller using RS232 interface

<div>
<img src="https://user-images.githubusercontent.com/54183150/80918265-061b7280-8d9f-11ea-8176-2a823d6c3d5a.jpg">
</div>

### Hardware
- Wemos D1 MINI
- MAX3232

```
Wemos D1 MINI : MAX3232
3V3: VCC
G: GND
D3: TXD
D4: RXD
```

### Command reference
https://www.lg.com/us/business/download/resources/BT00001837/UV340C-U_Install_Manual_170825.pdf

### ESPHome Configuration

To use this component, you need to include it as an external component in your ESPHome YAML configuration.

1.  **Copy the `lgtv_uart_external` directory** into your ESPHome configuration directory (the same directory where your `your_device.yaml` file is located).

2.  **Add the following to your ESPHome YAML file:**

    ```yaml
    external_components:
      - source:
          type: local
          path: lgtv_uart_external # This should be the name of the directory you copied

    # Example UART setup (adjust pins and ID as needed)
    uart:
      id: uart_bus
      baud_rate: 9600
      tx_pin: D3 # Or your TX pin
      rx_pin: D4 # Or your RX pin

    # Example binary sensor using the lgtv_uart_external platform
    binary_sensor:
      - platform: lgtv_uart_external
        name: "LGTV Power State" # You can customize this name
        id: lgtv_power # You can customize this ID
        uart_id: uart_bus # Ensure this matches the ID of your uart component
    ```

    Make sure to adjust the `path` under `external_components` if you named the directory differently. Also, ensure your `uart` configuration (like `id(uart_bus)`, `tx_pin`, `rx_pin`) matches your hardware setup. The `binary_sensor` example shows how to use the `lgtv_uart_external` platform to get the power state. Other functionalities are typically exposed as switches as shown in the example `lgtv.yaml` in this repository.
