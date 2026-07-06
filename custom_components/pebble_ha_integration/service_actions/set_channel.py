"""
set_channel service action for pebble_ha_integration.

This is the primary way automations drive the watch's dashboard: each call
updates one of the 10 HA channels and pushes the change to every WebSocket
connection currently subscribed via `pebble_dashboard/subscribe_channels`. See
HA_INTEGRATION_SPEC.md for the full payload shape this mirrors.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from custom_components.pebble_ha_integration.const import LOGGER

if TYPE_CHECKING:
    from custom_components.pebble_ha_integration.data import PebbleWatchConfigEntry
    from homeassistant.core import HomeAssistant, ServiceCall

# Fields the service accepts, matching HA_INTEGRATION_SPEC.md's per-channel
# payload shape exactly (minus `channel` itself, which is handled separately).
CHANNEL_FIELDS = (
    "value",
    "label",
    "kind",
    "unit",
    "min",
    "max",
    "style",
    "on_color",
    "off_color",
    "hide_when",
    "bg_color",
    "value_color",
    "label_color",
)


async def async_handle_set_channel(
    hass: HomeAssistant,
    entry: PebbleWatchConfigEntry,
    call: ServiceCall,
) -> None:
    """
    Handle the set_channel service action call.

    Args:
        hass: Home Assistant instance.
        entry: Config entry for the integration.
        call: Service call data - see CHANNEL_FIELDS for accepted fields.

    """
    channel = call.data["channel"]
    fields = {key: call.data[key] for key in CHANNEL_FIELDS if key in call.data}
    entry.runtime_data.channel_store.update_and_broadcast(channel, **fields)
    LOGGER.debug("set_channel: channel=%s fields=%s", channel, fields)
