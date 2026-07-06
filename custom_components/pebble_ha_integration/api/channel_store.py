"""In-memory store for the 10 HA -> watch dashboard channels.

Tracks the current state of each populated channel (see the "Payload shape" section
of HA_INTEGRATION_SPEC.md) and broadcasts updates to every WebSocket connection
currently subscribed via `pebble_dashboard/subscribe_channels`.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from custom_components.pebble_ha_integration.const import CHANNEL_MAX, CHANNEL_MIN
from homeassistant.components.websocket_api.connection import ActiveConnection
from homeassistant.components.websocket_api.messages import event_message
from homeassistant.core import callback

if TYPE_CHECKING:
    from collections.abc import Callable


class PebbleChannelStore:
    """Holds current channel state and the set of active subscriber connections."""

    def __init__(self) -> None:
        """Initialize an empty channel store with no populated channels or subscribers."""
        self._channels: dict[int, dict[str, Any]] = {}
        self._subscribers: dict[int, tuple[ActiveConnection, int]] = {}
        self._next_subscriber_key = 0

    @property
    def channels(self) -> list[dict[str, Any]]:
        """Return the payload for every currently-populated channel, sorted by number."""
        return [{"channel": channel, **fields} for channel, fields in sorted(self._channels.items())]

    @property
    def subscriber_count(self) -> int:
        """Return the number of connections currently subscribed to channel updates."""
        return len(self._subscribers)

    def update_and_broadcast(self, channel: int, **fields: Any) -> None:
        """Merge new field values into a channel and push the update to subscribers.

        Only the fields actually provided are changed - unset fields (label, kind,
        colors, ...) stay whatever they were last set to, matching the spec's
        "sticky" field semantics.
        """
        if not CHANNEL_MIN <= channel <= CHANNEL_MAX:
            msg = f"channel must be between {CHANNEL_MIN} and {CHANNEL_MAX}, got {channel}"
            raise ValueError(msg)

        current = self._channels.setdefault(channel, {})
        current.update({key: value for key, value in fields.items() if value is not None})

        event = {"channel": channel, **current}
        for connection, msg_id in self._subscribers.values():
            connection.send_message(event_message(msg_id, event))

    @callback
    def async_add_subscriber(
        self,
        connection: ActiveConnection,
        msg_id: int,
    ) -> Callable[[], None]:
        """Register a connection to receive future channel updates.

        Returns an unsubscribe callback suitable for `connection.subscriptions[msg_id]`,
        which Home Assistant calls automatically when the connection closes.
        """
        key = self._next_subscriber_key
        self._next_subscriber_key += 1
        self._subscribers[key] = (connection, msg_id)

        @callback
        def unsubscribe() -> None:
            self._subscribers.pop(key, None)

        return unsubscribe
