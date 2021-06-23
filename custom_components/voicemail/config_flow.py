"""Adds config flow for HA Voicemail."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.util import slugify

from .const import CONF_NAME
from .const import DOMAIN


class VoicemailFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for voicemail."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize."""
        self._errors = {}

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        self._errors = {}

        # Uncomment the next 2 lines if only a single instance of the integration is allowed:
        # if self._async_current_entries():
        #     return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:

            return self.async_create_entry(
                title=user_input[CONF_NAME],
                data={CONF_NAME: slugify(user_input[CONF_NAME])},
            )

        return await self._show_config_form(user_input)

    async def _show_config_form(self, user_input):  # pylint: disable=unused-argument
        """Show the configuration form to edit location data."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({vol.Required(CONF_NAME): str}),
            errors=self._errors,
        )

    # @staticmethod
    # @callback
    # def async_get_options_flow(config_entry):
    #     return VoicemailOptionsFlowHandler(config_entry)


# class VoicemailOptionsFlowHandler(config_entries.OptionsFlow):
#     """Config flow options handler for voicemail."""

#     def __init__(self, config_entry):
#         """Initialize HACS options flow."""
#         self.config_entry = config_entry
#         self.options = dict(config_entry.options)

#     async def async_step_init(self, user_input=None):  # pylint: disable=unused-argument
#         """Manage the options."""
#         return await self.async_step_user()

#     async def async_step_user(self, user_input=None):
#         """Handle a flow initialized by the user."""
#         if user_input is not None:
#             self.options.update(user_input)
#             return await self._update_options()

#         return self.async_show_form(
#             step_id="user",
#             data_schema=vol.Schema(
#                 {
#                     vol.Required(x, default=self.options.get(x, True)): bool
#                     for x in sorted(PLATFORMS)
#                 }
#             ),
#         )

#     async def _update_options(self):
#         """Update config entry options."""
#         return self.async_create_entry(
#             title=self.config_entry.data.get(CONF_USERNAME), data=self.options
#         )
