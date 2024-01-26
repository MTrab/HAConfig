"""Switches for Webasto Connect."""

import logging
from typing import Any, cast

from homeassistant.components import switch
from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import callback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)
from homeassistant.util import slugify as util_slugify

from .api import WebastoConnectUpdateCoordinator
from .base import WebastoConnectSwitchEntityDescription
from .const import ATTR_COORDINATOR, DOMAIN

LOGGER = logging.getLogger(__name__)

SWITCHES = [
    WebastoConnectSwitchEntityDescription(
        key="main_output",
        name="Output",
        entity_category=None,
        value_fn=lambda webasto: cast(bool, webasto.output_main),
        command_fn=lambda webasto, state: webasto.set_output_main(state),
        name_fn=lambda webasto: webasto.output_main_name,
        entity_registry_enabled_default=True,
    ),
    WebastoConnectSwitchEntityDescription(
        key="ventilation_mode",
        name="Ventilation Mode",
        entity_category=EntityCategory.CONFIG,
        value_fn=lambda webasto: cast(bool, webasto.is_ventilation),
        command_fn=lambda webasto, state: webasto.ventilation_mode(state),
        entity_registry_enabled_default=False,
    ),
    WebastoConnectSwitchEntityDescription(
        key="aux1_output",
        name="AUX1",
        entity_category=None,
        value_fn=lambda webasto: cast(bool, webasto.output_aux1),
        command_fn=lambda webasto, state: webasto.set_output_aux1(state),
        name_fn=lambda webasto: webasto.output_aux1_name,
        entity_registry_enabled_default=True,
    ),
    WebastoConnectSwitchEntityDescription(
        key="aux2_output",
        name="AUX2",
        entity_category=None,
        value_fn=lambda webasto: cast(bool, webasto.output_aux2),
        command_fn=lambda webasto, state: webasto.set_output_aux2(state),
        name_fn=lambda webasto: webasto.output_aux2_name,
        entity_registry_enabled_default=True,
    ),
]


async def async_setup_entry(hass, entry: ConfigEntry, async_add_devices):
    """Setup switch."""
    switches = []

    coordinator = hass.data[DOMAIN][entry.entry_id][ATTR_COORDINATOR]

    for swi in SWITCHES:
        LOGGER.debug("Testing '%s'", swi.name)
        if (
            isinstance(swi.name_fn, type(None))
            or swi.name_fn(coordinator.cloud) is not False
        ):
            entity = WebastoConnectSwitch(swi, coordinator)
            LOGGER.debug(
                "Adding switch '%s' with entity_id '%s'", swi.name, entity.entity_id
            )
            switches.append(entity)

    async_add_devices(switches)


class WebastoConnectSwitch(
    CoordinatorEntity[DataUpdateCoordinator[None]], SwitchEntity
):
    """Representation of a Webasto Connect switch."""

    def __init__(
        self,
        description: WebastoConnectSwitchEntityDescription,
        coordinator: WebastoConnectUpdateCoordinator,
    ) -> None:
        """Initialize a Webasto Connect switch."""
        super().__init__(coordinator)

        self.entity_description = description
        self._config = coordinator.entry
        self.coordinator = coordinator
        self._hass = coordinator.hass
        self._base_name = self.entity_description.name

        if not isinstance(self.entity_description.name_fn, type(None)):
            self._attr_name = self.entity_description.name_fn(coordinator.cloud)
        else:
            self._attr_name = self.entity_description.name

        self._attr_unique_id = util_slugify(
            f"{self._base_name}_{self._config.entry_id}"
        )

        self._attr_should_poll = False

        self._attr_device_info = {
            "identifiers": {(DOMAIN, self.coordinator.cloud.device_id)},
            "name": self.coordinator.cloud.name,
            "model": "ThermoConnect",
            "manufacturer": "Webasto",
        }

        self._handle_states()

        self.entity_id = switch.ENTITY_ID_FORMAT.format(
            util_slugify(f"{self.coordinator.cloud.name} {self._attr_name}")
        )

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._handle_states()
        self.async_write_ha_state()

    def _handle_states(self) -> None:
        """Handle the switch states."""
        if not isinstance(self.entity_description.name_fn, type(None)):
            self._attr_name = self.entity_description.name_fn(self.coordinator.cloud)

        self._attr_is_on = self.entity_description.value_fn(self.coordinator.cloud)

        if self.entity_description.key == "main_output":
            if self.coordinator.cloud.is_ventilation:
                self._attr_icon = "mdi:fan" if self._attr_is_on else "mdi:fan-off"
            else:
                self._attr_icon = (
                    "mdi:radiator" if self._attr_is_on else "mdi:radiator-off"
                )
        elif self.entity_description.key == "ventilation_mode":
            self._attr_icon = "mdi:fan" if self._attr_is_on else "mdi:fan-off"

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on the switch."""
        LOGGER.debug("Turning on %s", self.entity_id)
        await self._hass.async_add_executor_job(
            self.entity_description.command_fn, self.coordinator.cloud, True
        )
        await self.coordinator.async_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off the switch."""
        LOGGER.debug("Turning off %s", self.entity_id)
        await self._hass.async_add_executor_job(
            self.entity_description.command_fn, self.coordinator.cloud, False
        )
        await self.coordinator.async_refresh()
