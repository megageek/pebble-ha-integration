"""Service actions package for pebble_ha_integration."""

from __future__ import annotations

from typing import TYPE_CHECKING

import voluptuous as vol

from custom_components.pebble_ha_integration.const import CHANNEL_COLORS, CHANNEL_MAX, CHANNEL_MIN, DOMAIN
from custom_components.pebble_ha_integration.service_actions.set_channel import async_handle_set_channel
from homeassistant.core import ServiceCall
from homeassistant.exceptions import ServiceValidationError
from homeassistant.helpers import config_validation as cv

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

# Service action names - only used within service_actions module
SERVICE_SET_CHANNEL = "set_channel"

_COLOR_SELECTOR = vol.In(CHANNEL_COLORS)

SET_CHANNEL_SCHEMA = vol.Schema(
    {
        vol.Required("channel"): vol.All(int, vol.Range(min=CHANNEL_MIN, max=CHANNEL_MAX)),
        vol.Required("value"): vol.Any(int, cv.string),
        vol.Optional("label"): cv.string,
        vol.Optional("kind"): vol.In(("text", "numeric", "binary")),
        vol.Optional("unit"): cv.string,
        vol.Optional("min"): int,
        vol.Optional("max"): int,
        vol.Optional("style"): vol.In(("raw", "bar")),
        vol.Optional("on_color"): _COLOR_SELECTOR,
        vol.Optional("off_color"): _COLOR_SELECTOR,
        vol.Optional("hide_when"): vol.In(("none", "on", "off")),
        vol.Optional("bg_color"): _COLOR_SELECTOR,
        vol.Optional("value_color"): _COLOR_SELECTOR,
        vol.Optional("label_color"): _COLOR_SELECTOR,
    }
)


async def async_setup_services(hass: HomeAssistant) -> None:
    """
    Register services for the integration.

    Services are registered at component level (in async_setup) rather than
    per config entry. This is a Silver Quality Scale requirement and ensures:
    - Service action validation works correctly
    - Service actions are available even without config entries
    - Helpful error messages are provided
    """

    async def handle_set_channel(call: ServiceCall) -> None:
        """Handle the set_channel service call."""
        entries = hass.config_entries.async_entries(DOMAIN)
        if not entries:
            raise ServiceValidationError(
                translation_domain=DOMAIN,
                translation_key="not_configured",
            )
        await async_handle_set_channel(hass, entries[0], call)

    if not hass.services.has_service(DOMAIN, SERVICE_SET_CHANNEL):
        hass.services.async_register(
            DOMAIN,
            SERVICE_SET_CHANNEL,
            handle_set_channel,
            schema=SET_CHANNEL_SCHEMA,
        )
