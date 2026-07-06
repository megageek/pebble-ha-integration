"""
Entity package for pebble_ha_integration.

Architecture:
    All platform entities inherit from (PlatformEntity, PebbleWatchEntity).
    MRO order matters — platform-specific class first, then the integration base.
    Entities read data from coordinator.data and NEVER call the API client directly.
    Unique IDs follow the pattern: {entry_id}_{description.key}

See entity/base.py for the PebbleWatchEntity base class.
"""

from .base import PebbleWatchEntity

__all__ = ["PebbleWatchEntity"]
