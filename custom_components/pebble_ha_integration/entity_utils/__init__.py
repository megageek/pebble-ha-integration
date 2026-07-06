"""Entity utilities package for pebble_ha_integration."""

from .device_info import get_device_identifiers
from .dynamic_setup import async_setup_lazy_entities

__all__ = [
    "async_setup_lazy_entities",
    "get_device_identifiers",
]
