"""
API package for pebble_ha_integration.

Architecture:
    Three-layer data flow: Entities → Coordinator → API Client.
    Only the coordinator should call the API client. Entities must never
    import or call the API client directly.

Exception hierarchy:
    PebbleWatchApiClientError (base)
    ├── PebbleWatchApiClientCommunicationError (network/timeout)
    └── PebbleWatchApiClientAuthenticationError (401/403)

Coordinator exception mapping:
    ApiClientAuthenticationError → ConfigEntryAuthFailed (triggers reauth)
    ApiClientCommunicationError → UpdateFailed (auto-retry)
    ApiClientError             → UpdateFailed (auto-retry)
"""

from .client import (
    PebbleWatchApiClient,
    PebbleWatchApiClientAuthenticationError,
    PebbleWatchApiClientCommunicationError,
    PebbleWatchApiClientError,
)

__all__ = [
    "PebbleWatchApiClient",
    "PebbleWatchApiClientAuthenticationError",
    "PebbleWatchApiClientCommunicationError",
    "PebbleWatchApiClientError",
]
