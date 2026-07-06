"""WebSocket API commands implementing the Pebble dashboard protocol.

See HA_INTEGRATION_SPEC.md for the full wire contract these two commands implement:
`pebble_dashboard/subscribe_channels` (HA -> watch channel data) and
`pebble_dashboard/report_status` (watch -> HA battery/health/device-info reports).
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import voluptuous as vol

from custom_components.pebble_ha_integration.const import (
    DEVICE_INFO_FIELDS,
    DOMAIN,
    WS_TYPE_REPORT_STATUS,
    WS_TYPE_SUBSCRIBE_CHANNELS,
)
from custom_components.pebble_ha_integration.entity_utils.device_info import get_device_identifiers
from homeassistant.components import websocket_api
from homeassistant.components.websocket_api.connection import ActiveConnection
from homeassistant.components.websocket_api.decorators import websocket_command
from homeassistant.config_entries import ConfigEntryState
from homeassistant.core import callback
from homeassistant.helpers import device_registry as dr

if TYPE_CHECKING:
    from custom_components.pebble_ha_integration.data import PebbleWatchConfigEntry
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant


@callback
def async_register_websocket_commands(hass: HomeAssistant) -> None:
    """Register the two custom WebSocket API commands the phone bridge calls."""
    websocket_api.async_register_command(hass, handle_subscribe_channels)
    websocket_api.async_register_command(hass, handle_report_status)


def _get_loaded_entry(hass: HomeAssistant) -> PebbleWatchConfigEntry | None:
    """Return the single loaded Pebble Watch config entry, if one exists."""
    for entry in hass.config_entries.async_entries(DOMAIN):
        if entry.state is ConfigEntryState.LOADED:
            return entry
    return None


@websocket_command(
    {
        vol.Required("type"): WS_TYPE_SUBSCRIBE_CHANNELS,
    }
)
@callback
def handle_subscribe_channels(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Reply with current channel state and subscribe to future channel changes."""
    entry = _get_loaded_entry(hass)
    if entry is None:
        connection.send_error(msg["id"], "not_configured", "Pebble Watch integration is not set up")
        return

    channel_store = entry.runtime_data.channel_store
    connection.subscriptions[msg["id"]] = channel_store.async_add_subscriber(connection, msg["id"])
    connection.send_result(msg["id"], {"channels": channel_store.channels})


@websocket_command(
    {
        vol.Required("type"): WS_TYPE_REPORT_STATUS,
        vol.Required("status"): dict,
    }
)
@callback
def handle_report_status(
    hass: HomeAssistant,
    connection: ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Ingest a periodic status report, or the one-time device-info report, from the watch."""
    entry = _get_loaded_entry(hass)
    if entry is None:
        connection.send_error(msg["id"], "not_configured", "Pebble Watch integration is not set up")
        return

    status: dict[str, Any] = msg["status"]

    if any(field in status for field in DEVICE_INFO_FIELDS):
        _async_update_device_registry(hass, entry, status)

    entry.runtime_data.status_coordinator.async_ingest_status_report(status)
    connection.send_result(msg["id"])


@callback
def _async_update_device_registry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    status: dict[str, Any],
) -> None:
    """Apply the watch's one-time model/firmware report to its HA device entry."""
    device_registry = dr.async_get(hass)
    updates: dict[str, Any] = {}
    if "model" in status:
        updates["model"] = status["model"]
    if "firmware" in status:
        updates["sw_version"] = status["firmware"]

    device_registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers=get_device_identifiers(entry),
        manufacturer="Pebble",
        **updates,
    )
