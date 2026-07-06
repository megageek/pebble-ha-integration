"""
Coordinator package for pebble_ha_integration.

Package structure:
- base.py: PebbleWatchStatusCoordinator, a pure push sink for `report_status` reports
- data_processing.py: entity registry sync for the `disabled` measure-group field

For more information on coordinators:
https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
"""

from __future__ import annotations

from .base import PebbleWatchStatusCoordinator

__all__ = ["PebbleWatchStatusCoordinator"]
