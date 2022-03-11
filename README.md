# My Home Assistant configuration

## Home Assistant version
Home Assistant Supervised on Home Assistant OS 

## Hardware
ODroid N2+, 4GB RAM, 64GB eMMC
Conbee II
Aeotec Z-Wave stick gen5

## Supervisor Add-Ons
<ul>
  <li>Check Home Assistant Configuration</li>
  <li>ESPHome</li>
  <li>Frigate NVR</li>
  <li>Glances</li>
  <li>Grafana</li>
  <li>Home Assistant Google Drive Backup</li>
  <li>InfluxDB</li>
  <li>Log viewer</li>
  <li>MariaDB</li>
  <li>Mosquitto broker</li>
  <li>Nginx Proxy Manager</li>
  <li>RPC Shutdown</li>
  <li>Studio Code Server</li>
  <li>Terminal & SSH</li>
  <li>Traccar</li>
  <li>Z-Wave JS to MQTT</li>
  <li>Zigbee2MQTT</li>
</ul>

## Additional repositories
https://github.com/sabeechen/hassio-google-drive-backup<br>
https://esphome.io<br>
https://github.com/blakeblackshear/frigate-hass-addons<br>
https://github.com/zigbee2mqtt/hassio-zigbee2mqtt<br>
https://addons.community<br>

# Config specifics
## Config files
All config are seperated to different files located in /config/configurations<br>
Recently I've moved more towards making packages of my different solutions, rather than seperate entity integrations - hence more and more of my configuration will be in /config/configurations/packages

## Automations and scripts
All automations not part of a package are found in /config/automations.yaml and /config/scripts.yaml - all of those a made in Home Assistant GUI.<br>
If a automation or script have been merged as a part of a package, you'll find it in the respective files.

# HACS
I rely heavily on HACS for integrations and lovelace cards.

## Custom repositories
https://github.com/Radioh/ha_twitch_helix<br>
https://github.com/wxt9861/esxi_stats<br>

## Integrations
<ul>
  <li>HACS</li>
  <li>nordpool</li>
  <li>Places</li>
  <li>pyscript</li>
  <li>Scheduler component</li>
  <li>Variable</li>
  <li>iCal Sensor</li>
  <li>Google Home</li>
  <li>Power calculation</li>
  <li>ESXi Stats</li>
  <li>Landroid Cloud</li>
  <li>adaptive_lighting</li>
  <li>Homeassistant Generic Hygrostat</li>
  <li>Local Tuya</li>
  <li>Frigate</li>
  <li>Sonos Cloud</li>
  <li>pfSense integration for Home Assistant</li>
  <li>Twitch Helix</li>
</ul>

## Frontend
<ul>
  <li>Battery Entity Row</li>
  <li>Bar Card</li>
  <li>Flex Table - Highly customizable, Data visualization</li>
  <li>Multiline Text Input Card</li>
  <li>Config Template Card</li>
  <li>Text Divider Row</li>
  <li>Scheduler Card</li>
  <li>Lovelace Google Keep Card</li>
  <li>card-mod</li>
  <li>apexcharts-card</li>
  <li>auto-entities</li>
  <li>Restriction Card</li>
  <li>card-tools</li>
  <li>Midnight Theme</li>
  <li>mini-graph-card</li>
  <li>button-card</li>
  <li>layout-card</li>
  <li>Secondaryinfo Entity Row</li>
  <li>Frigate Card</li>
</ul>