"""Status-report binary sensors for pebble_ha_integration.

Both fields here are 0/1 integers on the wire (see HA_INTEGRATION_SPEC.md's
`pebble_dashboard/report_status` payload), so one generic entity class serves both.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from custom_components.pebble_ha_integration.entity import PebbleWatchEntity
from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.const import EntityCategory

if TYPE_CHECKING:
    from custom_components.pebble_ha_integration.coordinator import PebbleWatchStatusCoordinator

ENTITY_DESCRIPTIONS: tuple[BinarySensorEntityDescription, ...] = (
    BinarySensorEntityDescription(
        key="battery_charging",
        translation_key="battery_charging",
        entity_category=EntityCategory.DIAGNOSTIC,
        device_class=BinarySensorDeviceClass.BATTERY_CHARGING,
    ),
    BinarySensorEntityDescription(
        key="connected",
        translation_key="connected",
        entity_category=EntityCategory.DIAGNOSTIC,
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
    ),
)


class PebbleWatchStatusBinarySensor(BinarySensorEntity, PebbleWatchEntity):
    """Reports a single 0/1 field from the watch's report_status payload."""

    def __init__(
        self,
        coordinator: PebbleWatchStatusCoordinator,
        entity_description: BinarySensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entity_description)

    @property
    def is_on(self) -> bool:
        """Return true if the reported field is non-zero."""
        return bool(self.coordinator.data.get(self.entity_description.key))

    @property
    def available(self) -> bool:
        """Return whether the watch is currently reporting this field."""
        return super().available and self.entity_description.key in self.coordinator.data
