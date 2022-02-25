#pragma once
#include "esphome/core/component.h"
#include "esphome/core/helpers.h"
#include "esphome/components/api/custom_api_device.h"
#include "esphome.h"

namespace esphome {
namespace infopanel {

class InfoPanel : public PollingComponent, public api::CustomAPIDevice {
  public:
    void setup();
    void update() override;
    void loop() override;

  private:
    void on_event_update(int event_id, std::string text);
};
}
}