"""
API package for pebble_ha_integration.

Home Assistant is the WebSocket *server* in this integration - the phone-side
Pebble bridge connects in to HA's own `/api/websocket` endpoint, it's never HA
connecting out to a remote device. This package therefore has no HTTP client or
outbound-request exception hierarchy; it registers two custom WebSocket API
commands (see `websocket_commands.py`) and owns the in-memory channel state they
serve (see `channel_store.py`). See HA_INTEGRATION_SPEC.md for the wire contract.
"""

from .channel_store import PebbleChannelStore
from .websocket_commands import async_register_websocket_commands

__all__ = [
    "PebbleChannelStore",
    "async_register_websocket_commands",
]
