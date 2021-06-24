"""
Custom integration to integrate HA Voicemail with Home Assistant.

For more details about this integration, please refer to
https://github.com/danieldotnl/ha-voicemail
"""
import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Config
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .const import MACHINE_INSTANCE
from .const import PLATFORMS
from .const import STARTUP_MESSAGE
from .machine import Machine
from .schema import SERVICE_RECORD_WHEN_SCHEMA

SCAN_INTERVAL = timedelta(seconds=30)

_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_setup(hass: HomeAssistant, config: Config):
    """Set up this integration using YAML is not supported."""
    return True


async def _async_setup_services(hass: HomeAssistant, entry_id):
    async def async_record_when(service_call):
        _LOGGER.debug("Service call: %s", service_call)
        machine: Machine = hass.data[DOMAIN][entry_id][MACHINE_INSTANCE]
        await machine.async_record_when(service_call.data)

    async def async_play(service_call):
        machine: Machine = hass.data[DOMAIN][entry_id][MACHINE_INSTANCE]
        await machine.async_play()

    hass.services.async_register(
        DOMAIN, "record_when", async_record_when, SERVICE_RECORD_WHEN_SCHEMA
    )
    hass.services.async_register(DOMAIN, "play_all", async_play)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up this integration using UI."""

    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {}
        _LOGGER.info(STARTUP_MESSAGE)

    machine = Machine(hass, entry)

    data = {
        MACHINE_INSTANCE: machine,
    }
    hass.data[DOMAIN][entry.entry_id] = data
    await _async_setup_services(hass, entry.entry_id)

    # username = entry.data.get(CONF_USERNAME)
    # password = entry.data.get(CONF_PASSWORD)

    # session = async_get_clientsession(hass)
    # client = VoicemailApiClient(username, password, session)

    # coordinator = VoicemailDataUpdateCoordinator(hass, client=client)
    # await coordinator.async_refresh()

    # if not coordinator.last_update_success:
    #    raise ConfigEntryNotReady

    # hass.data[DOMAIN][entry.entry_id] = coordinator
    # _LOGGER.debug("Entry id = %s", entry.entry_id)

    # for platform in PLATFORMS:
    #     if entry.options.get(platform, True):
    #         coordinator.platforms.append(platform)
    #         hass.async_add_job(
    #             hass.config_entries.async_forward_entry_setup(entry, platform)
    #         )

    hass.config_entries.async_setup_platforms(entry, PLATFORMS)

    # entry.add_update_listener(async_reload_entry)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle removal of an entry."""
    # coordinator = hass.data[DOMAIN][entry.entry_id]
    # unloaded = all(
    #     await asyncio.gather(
    #         *[
    #             hass.config_entries.async_forward_entry_unload(entry, platform)
    #             for platform in PLATFORMS
    #             if platform in coordinator.platforms
    #         ]
    #     )
    # )
    # if unloaded:
    #     hass.data[DOMAIN].pop(entry.entry_id)

    # return unloaded
    return True


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
