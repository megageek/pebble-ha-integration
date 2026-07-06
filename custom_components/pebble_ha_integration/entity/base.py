"""
Base entity class for pebble_ha_integration.

This module provides the base entity class that all integration entities inherit from.
It handles common functionality like device info, unique IDs, and coordinator integration.

For more information on entities:
https://developers.home-assistant.io/docs/core/entity
https://developers.home-assistant.io/docs/core/entity/index/#common-properties
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from custom_components.pebble_ha_integration.coordinator import PebbleWatchStatusCoordinator
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

if TYPE_CHECKING:
    from homeassistant.helpers.entity import EntityDescription


class PebbleWatchEntity(CoordinatorEntity[PebbleWatchStatusCoordinator]):
    """
    Base entity class for pebble_ha_integration.

    All entities in this integration inherit from this class, which provides:
    - Automatic coordinator updates
    - Device info management
    - Unique ID generation
    - Entity naming conventions

    For more information:
    https://developers.home-assistant.io/docs/core/entity
    """

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: PebbleWatchStatusCoordinator,
        entity_description: EntityDescription,
    ) -> None:
        """
        Initialize the base entity.

        Args:
            coordinator: The status coordinator for this entity.
            entity_description: The entity description defining characteristics.

        """
        super().__init__(coordinator)
        self.entity_description = entity_description
        # Include entity description key in unique_id to support multiple entities
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_{entity_description.key}"
        # model/sw_version are deliberately omitted here - they arrive asynchronously
        # from the watch's one-time device-info report and are applied directly to
        # the device registry (see api/websocket_commands.py) rather than through a
        # static DeviceInfo set once at entity-add time.
        self._attr_device_info = DeviceInfo(
            identifiers={
                (
                    coordinator.config_entry.domain,
                    coordinator.config_entry.entry_id,
                ),
            },
            name=coordinator.config_entry.title,
            manufacturer="Pebble",
        )
