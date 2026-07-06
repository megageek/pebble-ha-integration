"""Binary sensor platform for pebble_ha_integration."""

from __future__ import annotations

from typing import TYPE_CHECKING

from custom_components.pebble_ha_integration.const import PARALLEL_UPDATES as PARALLEL_UPDATES
from custom_components.pebble_ha_integration.entity_utils import async_setup_lazy_entities

from .status import ENTITY_DESCRIPTIONS as STATUS_DESCRIPTIONS, PebbleWatchStatusBinarySensor

if TYPE_CHECKING:
    from custom_components.pebble_ha_integration.data import PebbleWatchConfigEntry
    from homeassistant.components.binary_sensor import BinarySensorEntityDescription
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

# Combine all entity descriptions from different modules
ENTITY_DESCRIPTIONS: tuple[BinarySensorEntityDescription, ...] = (*STATUS_DESCRIPTIONS,)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: PebbleWatchConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the binary_sensor platform.

    Entities are added lazily as the watch's status reports first mention them
    (see entity_utils/dynamic_setup.py) rather than all being created up front.
    """
    async_setup_lazy_entities(
        entry.runtime_data.status_coordinator,
        async_add_entities,
        [(description, PebbleWatchStatusBinarySensor) for description in STATUS_DESCRIPTIONS],
    )
