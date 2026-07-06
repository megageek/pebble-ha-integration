"""Constants for pebble_ha_integration."""

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

# Integration metadata
DOMAIN = "pebble_ha_integration"

# Platform parallel updates - applied to all platforms
PARALLEL_UPDATES = 1

# WebSocket API command names - must match HA_INTEGRATION_SPEC.md and the
# phone-side HA_SUBSCRIBE_COMMAND constant exactly.
WS_TYPE_SUBSCRIBE_CHANNELS = "pebble_dashboard/subscribe_channels"
WS_TYPE_REPORT_STATUS = "pebble_dashboard/report_status"

# There are exactly 10 HA channels on the watchface (CHANNEL_HA_1..CHANNEL_HA_10).
CHANNEL_MIN = 1
CHANNEL_MAX = 10

# Which report_status field(s) each measure group (battery, steps, activity, sleep,
# heart_rate, connected, device_info - the values the `disabled` status field
# names) controls, for the entity registry enable/disable sync. model/firmware are
# intentionally absent - they update the device registry, not an entity.
MEASURE_GROUP_KEYS: dict[str, tuple[str, ...]] = {
    "battery": ("battery_percent", "battery_charging"),
    "steps": ("steps",),
    "activity": ("active_seconds", "distance_meters", "active_kcal", "resting_kcal"),
    "sleep": ("sleep_seconds", "sleep_restful_seconds"),
    "heart_rate": ("heart_rate_bpm",),
    "connected": ("connected",),
    "device_info": ("color",),
}

# Shared color palette accepted by on_color/off_color/bg_color/value_color/label_color.
CHANNEL_COLORS = (
    "red",
    "orange",
    "yellow",
    "green",
    "blue",
    "purple",
    "white",
    "gray",
)

# Status report field holding the comma-separated disabled measure-group names.
STATUS_FIELD_DISABLED = "disabled"

# Device-info-only fields, sent once at watch startup in their own report_status
# message, never combined with the periodic status fields above.
DEVICE_INFO_FIELDS = ("model", "firmware", "color")
