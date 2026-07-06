"""
Config flow for pebble_ha_integration.

There is nothing to configure - the phone brings its own Home Assistant
long-lived access token when it connects, entirely outside this integration's
control (see HA_INTEGRATION_SPEC.md). The `user` step is a bare confirmation
that creates the single config entry `manifest.json`'s `single_config_entry`
flag limits this integration to.

For more information:
https://developers.home-assistant.io/docs/config_entries_config_flow_handler
"""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from custom_components.pebble_ha_integration.const import DOMAIN
from homeassistant import config_entries


class PebbleWatchConfigFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """
    Handle a config flow for pebble_ha_integration.

    For more details:
    https://developers.home-assistant.io/docs/config_entries_config_flow_handler
    """

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> config_entries.ConfigFlowResult:
        """
        Handle a flow initialized by the user.

        Args:
            user_input: The user input from the config flow form, or None for initial display.

        Returns:
            The config flow result, either showing the confirmation form or creating the entry.

        """
        if user_input is not None:
            return self.async_create_entry(title="Pebble Watch", data={})

        return self.async_show_form(step_id="user", data_schema=vol.Schema({}))


__all__ = ["PebbleWatchConfigFlowHandler"]
