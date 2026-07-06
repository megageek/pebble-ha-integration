"""
Custom integration to integrate pebble_ha_integration with Home Assistant.

This integration registers two custom WebSocket API commands that implement the
Pebble dashboard protocol (see HA_INTEGRATION_SPEC.md):
- `pebble_dashboard/subscribe_channels`: pushes HA data out to the watch as up to
  10 numbered "channels", set dynamically via the `set_channel` service action.
- `pebble_dashboard/report_status`: receives battery/health/device-info reports
  from the watch, which become sensor/binary_sensor entities created lazily as
  each measure is first reported.

For more details about this integration, please refer to:
https://github.com/megageek/pebble-ha-integration

For integration development guidelines:
https://developers.home-assistant.io/docs/creating_integration_manifest
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.const import Platform
import homeassistant.helpers.config_validation as cv
from homeassistant.loader import async_get_loaded_integration

from .api import PebbleChannelStore, async_register_websocket_commands
from .const import DOMAIN, LOGGER
from .coordinator import PebbleWatchStatusCoordinator
from .data import PebbleWatchData
from .service_actions import async_setup_services

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .data import PebbleWatchConfigEntry

PLATFORMS: list[Platform] = [
    Platform.BINARY_SENSOR,
    Platform.SENSOR,
]

# This integration is configured via config entries only
CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """
    Set up the integration.

    Called once at Home Assistant startup. Registers the two custom WebSocket API
    commands and the `set_channel` service action - both are hass-global, not tied
    to a specific config entry, so they must be registered here rather than in
    async_setup_entry() (Silver Quality Scale requirement for services, and the
    natural place for WebSocket commands too since only one command of each name
    can ever be registered).

    Args:
        hass: The Home Assistant instance.
        config: The Home Assistant configuration.

    Returns:
        True if setup was successful.

    """
    async_register_websocket_commands(hass)
    await async_setup_services(hass)
    return True


async def async_setup_entry(
    hass: HomeAssistant,
    entry: PebbleWatchConfigEntry,
) -> bool:
    """
    Set up this integration using UI.

    Unlike a typical polling integration, there is nothing to fetch at setup time -
    the channel store starts empty and the status coordinator starts with no data;
    both are populated reactively as WebSocket commands arrive from the phone.

    Args:
        hass: The Home Assistant instance.
        entry: The config entry being set up.

    Returns:
        True if setup was successful.

    For more information:
    https://developers.home-assistant.io/docs/config_entries_index/#setting-up-an-entry
    """
    status_coordinator = PebbleWatchStatusCoordinator(
        hass=hass,
        logger=LOGGER,
        name=DOMAIN,
        config_entry=entry,
        update_interval=None,
    )

    entry.runtime_data = PebbleWatchData(
        channel_store=PebbleChannelStore(),
        status_coordinator=status_coordinator,
        integration=async_get_loaded_integration(hass, entry.domain),
    )

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: PebbleWatchConfigEntry,
) -> bool:
    """
    Unload a config entry.

    This is called when the integration is being removed or reloaded.
    It ensures proper cleanup of all platform entities.

    Args:
        hass: The Home Assistant instance.
        entry: The config entry being unloaded.

    Returns:
        True if unload was successful.

    For more information:
    https://developers.home-assistant.io/docs/config_entries_index/#unloading-entries
    """
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_reload_entry(
    hass: HomeAssistant,
    entry: PebbleWatchConfigEntry,
) -> None:
    """
    Reload config entry.

    This is called when the integration configuration or options have changed.
    It unloads and then reloads the integration with the new configuration.

    Args:
        hass: The Home Assistant instance.
        entry: The config entry being reloaded.

    For more information:
    https://developers.home-assistant.io/docs/config_entries_index/#reloading-entries
    """
    await hass.config_entries.async_reload(entry.entry_id)
