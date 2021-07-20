from .const import MESSAGE_UPDATE_SIGNAL
from .message import Message


def message_update_signal(entry_id):
    return f"{MESSAGE_UPDATE_SIGNAL}_{entry_id}"


def convert_raw_messages(raw_messages):
    messages = []
    for raw_message in raw_messages:
        messages.append(
            Message(
                raw_message.get("name"), raw_message["service"], raw_message["data"]
            )
        )

    return messages
