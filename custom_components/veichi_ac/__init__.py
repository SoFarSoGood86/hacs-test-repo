from .const import DOMAIN, PLATFORMS
from .hub import VeichiHub

async def async_setup_entry(hass, entry):
    hub = VeichiHub(entry.data)
    await hass.async_add_executor_job(hub.connect)
    hub.start_watchdogs()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = hub

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    hass.services.async_register(DOMAIN, "start", lambda c: hub.start())
    hass.services.async_register(DOMAIN, "stop", lambda c: hub.stop())
    hass.services.async_register(DOMAIN, "emergency_stop", lambda c: hub.stop())
    hass.services.async_register(
        DOMAIN, "ramp_safe",
        lambda c: hub.ramp_safe(
            c.data["frequency"],
            c.data.get("step", 5),
            c.data.get("delay", 2)
        )
    )

    return True