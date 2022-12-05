import logging

from .const import (
    CONF_CLIENT,
    CONF_CONSUMPTION,
    CONF_PACKAGES,
    CONF_PLATFORM,
    CONF_USER,
    DOMAIN,
    UPDATE_INTERVAL,
)
from homeassistant.const import DEVICE_CLASS_MONETARY

from datetime import datetime, timedelta

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

_LOGGER = logging.getLogger(__name__)

HA_UNIT_OF_MEASUREMENT_SUBSCRIPTION = "DKK"


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Setup sensor platform"""

    async def async_update_data():
        client = hass.data[DOMAIN][CONF_CLIENT]
        await hass.async_add_executor_job(client.update)

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=CONF_PLATFORM,
        update_method=async_update_data,
        update_interval=timedelta(minutes=UPDATE_INTERVAL),
    )

    # Immediate refresh
    await coordinator.async_request_refresh()

    # Add the sensors
    client = hass.data[DOMAIN][CONF_CLIENT]
    entities = []

    for subscription in client.getSubscriptions():
        entities.append(SubscriptionSensor(hass, coordinator, subscription))

        if hass.data[DOMAIN][CONF_CONSUMPTION]:
            # Have we stated 'packages' in the config?
            if CONF_PACKAGES in hass.data[DOMAIN][CONF_CONSUMPTION]:

                # Loop over every consumable in the subscription
                for consumable in subscription.getConsumables():
                    entities.append(
                        ConsumptionSensor(
                            hass, coordinator, consumable, subscription.getName()
                        )
                    )

            # Have we stated 'user' in the config?
            if CONF_USER in hass.data[DOMAIN][CONF_CONSUMPTION]:
                for user in subscription.getUsers():
                    for consumable in user.getConsumables():
                        entities.append(
                            ConsumptionSensor(
                                hass, coordinator, consumable, user.getUsername()
                            )
                        )

    async_add_entities(entities)


class ConsumptionSensor(SensorEntity):
    def __init__(self, hass, coordinator, consumption, parentName) -> None:
        self._hass = hass
        self._coordinator = coordinator
        self._consumption = consumption
        self._name = f"{consumption.getName()} ({parentName})"
        self._unique_id = parentName + "_" + self._name

    @property
    def name(self) -> str:
        return self._name

    @property
    def state(self):
        return self._consumption.getUsed()

    @property
    def unit_of_measurement(self) -> str:
        return self._consumption.getUnit()

    @property
    def extra_state_attributes(self):
        # Prepare a dictionary with attributes
        attr = {
            "total": self._consumption.getTotal(),
            "left": self._consumption.getLeft(),
        }

        return attr

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def should_poll(self):
        """No need to poll. Coordinator notifies entity of updates."""
        return False

    @property
    def available(self):
        """Return if entity is available."""
        return self._coordinator.last_update_success

    async def async_update(self):
        """Update the entity. Only used by the generic entity update service."""
        await self._coordinator.async_request_refresh()

    async def async_added_to_hass(self):
        """When entity is added to hass."""
        self.async_on_remove(
            self._coordinator.async_add_listener(self.async_write_ha_state)
        )


class SubscriptionSensor(SensorEntity):
    def __init__(self, hass, coordinator, subscription) -> None:
        self._hass = hass
        self._coordinator = coordinator
        self._subscription = subscription

    @property
    def name(self) -> str:
        return self._subscription.getName()

    @property
    def state(self):
        return self._subscription.getBalance()

    @property
    def unit_of_measurement(self) -> str:
        return HA_UNIT_OF_MEASUREMENT_SUBSCRIPTION

    @property
    def extra_state_attributes(self):
        attr = {
            "active": self._subscription.getActive(),
            "payment_type": self._subscription.getPaymentType(),
            "recharge_ticket amount": self._subscription.getRechargeTicketAmount(),
            "auto_adjust_amount": self._subscription.getAutoAdjustAmount(),
        }

        return attr

    @property
    def unique_id(self):
        return DOMAIN + "_" + self._subscription.getName()

    @property
    def device_class(self) -> str:
        return DEVICE_CLASS_MONETARY

    @property
    def should_poll(self):
        """No need to poll. Coordinator notifies entity of updates."""
        return False

    @property
    def available(self):
        """Return if entity is available."""
        return self._coordinator.last_update_success

    async def async_update(self):
        """Update the entity. Only used by the generic entity update service."""
        await self._coordinator.async_request_refresh()

    async def async_added_to_hass(self):
        """When entity is added to hass."""
        self.async_on_remove(
            self._coordinator.async_add_listener(self.async_write_ha_state)
        )
