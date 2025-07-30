#include "esphome/core/component.h"
#include "esphome/components/uart/uart.h"
#include "esphome/components/binary_sensor/binary_sensor.h"
#include "esphome/core/log.h"

namespace esphome {
namespace lgtv_uart {

#define LGTV_BUFFER_LEN   64

class LGTVUARTComponent : public esphome::Component, public esphome::uart::UARTDevice, public esphome::binary_sensor::BinarySensor {
  protected:
	uint8_t uart_buffer[LGTV_BUFFER_LEN]{0};
	int offset = 0;
	
  public:
	LGTVUARTComponent(esphome::uart::UARTComponent *parent) : UARTDevice(parent) {}

	void setup() override {
	// nothing to do here
	}
	void loop() override {

		while (available()) {
			char c = read();
			this->uart_buffer[offset++] = c;
			if (offset > LGTV_BUFFER_LEN - 1) {
				offset = 0;
				break;
			}

			if (c == 'x') {
				this->uart_buffer[offset] = '\0';
				ESP_LOGD("LGTVUART", "[%d] %s", offset, this->uart_buffer);
				if (memcmp(this->uart_buffer, "a ", 2) == 0) {
					if (memcmp(this->uart_buffer + 5, "OK01x", 5) == 0)
						publish_state(true);
					else if (memcmp(this->uart_buffer + 5, "OK00x", 5) == 0)
						publish_state(false);
				}
				offset = 0;
				break;
			}
		
		}

	}
};

}  // namespace lgtv_uart
}  // namespace esphome
