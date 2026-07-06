"""Diagnostics support for pebble_ha_integration.

Learn more about diagnostics:
https://developers.home-assistant.io/docs/core/integration_diagnostics
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.helpers import device_registry as dr, entity_registry as er
from homeassistant.helpers.redact import async_redact_data

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .data import PebbleWatchConfigEntry

# Nothing sensitive is stored in entry.data/entry.options today (there are no
# credentials in this design - the phone brings its own HA token), but keep the
# usual set redacted defensively in case that ever changes.
TO_REDACT = {"token", "access_token", "api_key"}


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant,
    entry: PebbleWatchConfigEntry,
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    channel_store = entry.runtime_data.channel_store
    status_coordinator = entry.runtime_data.status_coordinator
    integration = entry.runtime_data.integration

    device_reg = dr.async_get(hass)
    entity_reg = er.async_get(hass)

    devices = dr.async_entries_for_config_entry(device_reg, entry.entry_id)
    device_info = [
        {
            "id": device.id,
            "name": device.name,
            "manufacturer": device.manufacturer,
            "model": device.model,
            "sw_version": device.sw_version,
            "entities": [
                {
                    "entity_id": entity.entity_id,
                    "disabled_by": entity.disabled_by.value if entity.disabled_by else None,
                }
                for entity in er.async_entries_for_device(entity_reg, device.id)
            ],
        }
        for device in devices
    ]

    integration_info = {
        "name": integration.name,
        "version": integration.version,
        "domain": integration.domain,
    }

    entry_info = {
        "entry_id": entry.entry_id,
        "state": str(entry.state),
        "data": async_redact_data(entry.data, TO_REDACT),
        "options": async_redact_data(entry.options, TO_REDACT),
    }

    # Status values aren't dumped verbatim - some (heart rate, steps, sleep) are
    # personal health data - just which measures are currently being reported.
    status_info = {
        "reported_keys": sorted((status_coordinator.data or {}).keys()),
    }

    channel_info = {
        "channels": channel_store.channels,
        "subscriber_count": channel_store.subscriber_count,
    }

    return {
        "entry": entry_info,
        "integration": integration_info,
        "status": status_info,
        "channels": channel_info,
        "devices": device_info,
    }
