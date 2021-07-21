from .const import MESSAGE_UPDATE_SIGNAL
from .message import Message


def message_update_signal(entry_id):
    return f"{MESSAGE_UPDATE_SIGNAL}_{entry_id}"


def convert_raw_messages(raw_messages):
    messages = []
    for raw_message in raw_messages:
        messages.append(
            Message(
                name=raw_message.get("name"),
                service=raw_message["service"],
                data=raw_message["data"],
                created=raw_message.get("created"),
                uid=raw_message.get("uid"),
                expires=raw_message.get("expires"),
            )
        )

    return messages
