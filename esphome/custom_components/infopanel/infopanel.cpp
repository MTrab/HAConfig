#include "infopanel.h"
#include "esphome/core/log.h"

namespace esphome {
namespace infopanel {

static const char *TAG = "infopanel";

void InfoPanel::setup() {
  register_service(&InfoPanel::on_event_update, "event_update", {"event_id", "text"});
}

void InfoPanel::loop() {

}

void InfoPanel::update() {

}

void InfoPanel::on_event_update(int event_id, std::string text) {
  ESP_LOGD(TAG, "Event id %i returned %s", event_id, text.c_str());

  //call_homeassistant_service("homeassistant.service");
}

}
}