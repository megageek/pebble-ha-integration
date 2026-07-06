"""
Push-based status coordinator for pebble_ha_integration.

Unlike a typical DataUpdateCoordinator, this coordinator never polls anything - the
watch pushes battery/health/device-info reports to Home Assistant via the
`pebble_dashboard/report_status` WebSocket command (see `api/websocket_commands.py`),
which calls `async_ingest_status_report()` below every time a report arrives. See
HA_INTEGRATION_SPEC.md for the report shape and field semantics.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from custom_components.pebble_ha_integration.const import LOGGER
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .data_processing import async_sync_disabled_entities

if TYPE_CHECKING:
    from custom_components.pebble_ha_integration.data import PebbleWatchConfigEntry


class PebbleWatchStatusCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """
    Distributes watch status reports to entities.

    Pure push: constructed with `update_interval=None` and `_async_update_data` is
    never implemented or called, since there is nothing to poll - the watch decides
    when it reports in (startup, every battery change, once a minute, and
    immediately on a reporting-toggle change).

    Attributes:
        config_entry: The config entry for this integration instance.

    """

    config_entry: PebbleWatchConfigEntry

    def async_ingest_status_report(self, status: dict[str, Any]) -> None:
        """
        Merge a new (possibly partial) status report and notify entities.

        Every field is optional per the spec - a field's absence just means that
        measure wasn't accessible on the watch at report time, so previously known
        fields not present in this report are preserved rather than dropped.

        Args:
            status: The `status` payload from a `pebble_dashboard/report_status`
                WebSocket command, either a periodic report or the one-time
                device-info report.

        """
        old_status = self.data or {}
        merged = {**old_status, **status}
        LOGGER.debug("Ingested status report: %s", status)
        async_sync_disabled_entities(self.hass, self.config_entry, old_status, merged)
        self.async_set_updated_data(merged)
