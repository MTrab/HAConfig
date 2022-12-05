import logging

from .greentel import greentel
from .const import (
    DOMAIN,
    CONF_CLIENT,
    CONF_CONSUMPTION,
    CONF_PASSWORD,
    CONF_PHONENUMBER,
    CONF_PLATFORM,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass, config):
    conf = config.get(DOMAIN)
    if conf is None:
        return True

    _LOGGER.debug(CONF_CONSUMPTION + ": " + str(conf.get(CONF_CONSUMPTION, [])))

    # Initialize the Client
    client = greentel(conf.get(CONF_PHONENUMBER), conf.get(CONF_PASSWORD))
    hass.data[DOMAIN] = {
        CONF_CLIENT: client,
        CONF_CONSUMPTION: conf.get(CONF_CONSUMPTION, []),
    }

    # Add sensors
    hass.async_create_task(
        hass.helpers.discovery.async_load_platform(CONF_PLATFORM, DOMAIN, conf, config)
    )

    # Initialization was successful.
    return True
