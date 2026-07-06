"""Helper for platforms that add entities lazily as new status data appears.

Per HA_INTEGRATION_SPEC.md, a status measure that has never been reported (no
sensor hardware, no permission, or the user has it disabled) should have no
entity at all - not an entity pre-created and gated on `available`. Both the
sensor and binary_sensor platforms share this "add on first sight" behavior.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.core import callback

if TYPE_CHECKING:
    from collections.abc import Iterable

    from custom_components.pebble_ha_integration.coordinator import PebbleWatchStatusCoordinator
    from custom_components.pebble_ha_integration.entity import PebbleWatchEntity
    from homeassistant.helpers.entity import EntityDescription
    from homeassistant.helpers.entity_platform import AddEntitiesCallback


@callback
def async_setup_lazy_entities(
    coordinator: PebbleWatchStatusCoordinator,
    async_add_entities: AddEntitiesCallback,
    descriptions: Iterable[tuple[EntityDescription, type[PebbleWatchEntity]]],
) -> None:
    """Add entities for status keys as they are first reported.

    Runs once immediately (covering data already present after a reload) and again
    on every subsequent coordinator update, adding an entity only the first time
    its description's key actually appears in `coordinator.data`.
    """
    added_keys: set[str] = set()

    @callback
    def _check_new_entities() -> None:
        data = coordinator.data or {}
        new_entities = [
            entity_class(coordinator, description)
            for description, entity_class in descriptions
            if description.key in data and description.key not in added_keys
        ]
        if new_entities:
            added_keys.update(entity.entity_description.key for entity in new_entities)
            async_add_entities(new_entities)

    coordinator.async_add_listener(_check_new_entities)
    _check_new_entities()
