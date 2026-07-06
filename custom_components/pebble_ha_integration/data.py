"""
Custom types for pebble_ha_integration.

This module defines the runtime data structure attached to the config entry.
Access pattern: entry.runtime_data.channel_store / entry.runtime_data.status_coordinator

The PebbleWatchConfigEntry type alias is used throughout the integration
for type-safe access to the config entry's runtime data.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from .api import PebbleChannelStore
    from .coordinator import PebbleWatchStatusCoordinator


type PebbleWatchConfigEntry = ConfigEntry[PebbleWatchData]


@dataclass
class PebbleWatchData:
    """Runtime data for pebble_ha_integration config entries.

    Stored as entry.runtime_data after successful setup.
    Provides typed access to the channel store and status coordinator instances.
    """

    channel_store: PebbleChannelStore
    status_coordinator: PebbleWatchStatusCoordinator
    integration: Integration
