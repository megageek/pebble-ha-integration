"""Device info utilities for pebble_ha_integration."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry


def get_device_identifiers(config_entry: ConfigEntry) -> set[tuple[str, str]]:
    """
    Get device identifiers for a config entry.

    Args:
        config_entry: The config entry

    Returns:
        A set of device identifier tuples

    Example:
        >>> identifiers = get_device_identifiers(config_entry)
        >>> # Returns: {('pebble_ha_integration', 'entry_id_value')}
    """
    return {(config_entry.domain, config_entry.entry_id)}
