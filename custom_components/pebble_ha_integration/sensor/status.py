"""Status-report sensors for pebble_ha_integration.

Every sensor here is a plain pass-through of one field from the watch's
`pebble_dashboard/report_status` payload (see HA_INTEGRATION_SPEC.md) - the
EntityDescription's device_class/unit/state_class do all the formatting work, so
one generic entity class serves all of them.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from custom_components.pebble_ha_integration.entity import PebbleWatchEntity
from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorEntityDescription, SensorStateClass
from homeassistant.const import PERCENTAGE, EntityCategory, UnitOfLength, UnitOfTime

if TYPE_CHECKING:
    from custom_components.pebble_ha_integration.coordinator import PebbleWatchStatusCoordinator

ENTITY_DESCRIPTIONS: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="battery_percent",
        translation_key="battery_percent",
        entity_category=EntityCategory.DIAGNOSTIC,
        device_class=SensorDeviceClass.BATTERY,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="steps",
        translation_key="steps",
        icon="mdi:walk",
        native_unit_of_measurement="steps",
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="active_seconds",
        translation_key="active_seconds",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.SECONDS,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="distance_meters",
        translation_key="distance_meters",
        device_class=SensorDeviceClass.DISTANCE,
        native_unit_of_measurement=UnitOfLength.METERS,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="active_kcal",
        translation_key="active_kcal",
        icon="mdi:fire",
        native_unit_of_measurement="kcal",
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="resting_kcal",
        translation_key="resting_kcal",
        icon="mdi:fire",
        native_unit_of_measurement="kcal",
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="sleep_seconds",
        translation_key="sleep_seconds",
        icon="mdi:sleep",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.SECONDS,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="sleep_restful_seconds",
        translation_key="sleep_restful_seconds",
        icon="mdi:sleep",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.SECONDS,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="heart_rate_bpm",
        translation_key="heart_rate_bpm",
        icon="mdi:heart-pulse",
        native_unit_of_measurement="bpm",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="color",
        translation_key="color",
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:palette-outline",
    ),
)


class PebbleWatchStatusSensor(SensorEntity, PebbleWatchEntity):
    """Reports a single field from the watch's report_status payload."""

    def __init__(
        self,
        coordinator: PebbleWatchStatusCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entity_description)

    @property
    def native_value(self) -> int | str | None:
        """Return the current value of this status field."""
        return self.coordinator.data.get(self.entity_description.key)

    @property
    def available(self) -> bool:
        """Return whether the watch is currently reporting this field."""
        return super().available and self.entity_description.key in self.coordinator.data
