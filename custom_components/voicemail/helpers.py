from .const import MESSAGE_UPDATE_SIGNAL


def message_update_signal(entry_id):
    return f"{MESSAGE_UPDATE_SIGNAL}_{entry_id}"
