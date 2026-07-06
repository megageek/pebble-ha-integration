"""
Entity registry sync for the watch's `disabled` measure-group reporting.

HA_INTEGRATION_SPEC.md distinguishes two reasons a status field might be missing
from a report:

- The user explicitly turned that measure group off in the watchface's Clay config
  (named in the `disabled` field) - the corresponding entity should be
  registry-disabled, since it represents deliberate user intent.
- The field is merely inaccessible right now (no HR sensor, no Health permission,
  or it's simply never been reported yet) - an entity for it is only ever created
  once real data arrives (see the sensor/binary_sensor platforms), so there's
  nothing to disable in that case.

This module handles only the first case, diffing `disabled` between reports.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from custom_components.pebble_ha_integration.const import DOMAIN, MEASURE_GROUP_KEYS, STATUS_FIELD_DISABLED
from homeassistant.helpers import entity_registry as er

if TYPE_CHECKING:
    from custom_components.pebble_ha_integration.data import PebbleWatchConfigEntry
    from homeassistant.core import HomeAssistant


def _disabled_groups(status: dict[str, Any]) -> set[str]:
    """Parse the comma-separated `disabled` field into a set of group names."""
    raw = status.get(STATUS_FIELD_DISABLED, "")
    return {group for group in raw.split(",") if group}


def async_sync_disabled_entities(
    hass: HomeAssistant,
    entry: PebbleWatchConfigEntry,
    old_status: dict[str, Any],
    new_status: dict[str, Any],
) -> None:
    """
    Disable/re-enable entities whose measure group just entered/left `disabled`.

    Args:
        hass: The Home Assistant instance.
        entry: The config entry that owns the affected entities.
        old_status: The previously merged status data (before this report).
        new_status: The newly merged status data (including this report).

    """
    old_disabled = _disabled_groups(old_status)
    new_disabled = _disabled_groups(new_status)
    if old_disabled == new_disabled:
        return

    registry = er.async_get(hass)
    for group, keys in MEASURE_GROUP_KEYS.items():
        newly_disabled = group in new_disabled and group not in old_disabled
        newly_enabled = group in old_disabled and group not in new_disabled
        if not (newly_disabled or newly_enabled):
            continue

        for key in keys:
            unique_id = f"{entry.entry_id}_{key}"
            entity_id = registry.async_get_entity_id("sensor", DOMAIN, unique_id) or registry.async_get_entity_id(
                "binary_sensor", DOMAIN, unique_id
            )
            if entity_id is None:
                continue
            registry.async_update_entity(
                entity_id,
                disabled_by=er.RegistryEntryDisabler.INTEGRATION if newly_disabled else None,
            )
