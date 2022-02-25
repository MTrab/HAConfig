class InfoPanelEvent : public PollingComponent, public TextSensor, public CustomAPIDevice {
 public:
  // constructor
  InfoPanelEvent() : PollingComponent(15000) {}

  void setup() override {
      register_service(&InfoPanelEvent::on_event_update, "event_update", {"event_id", "text"});
  }
  void update() override {
    //call_homeassistant_service("homeassistant.service");
  }

  void on_event_update(int event_id, std::string text) {
    ESP_LOGD("InfoPanel", "Event id %i returned %s", event_id, text.c_str());

    //call_homeassistant_service("homeassistant.service");
  }
};