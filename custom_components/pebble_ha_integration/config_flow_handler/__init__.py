"""
Config flow handler package for pebble_ha_integration.

Package structure:
------------------
- config_flow.py: The (single, confirmation-only) configuration flow

Usage:
------
The main config flow handler is imported in config_flow.py at the integration root:

    from .config_flow_handler import PebbleWatchConfigFlowHandler

For more information:
https://developers.home-assistant.io/docs/config_entries_config_flow_handler
"""

from __future__ import annotations

from .config_flow import PebbleWatchConfigFlowHandler

__all__ = [
    "PebbleWatchConfigFlowHandler",
]
