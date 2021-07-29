from .const import MESSAGE_UPDATE_SIGNAL
from .message import Message


def message_update_signal(entry_id):
    return f"{MESSAGE_UPDATE_SIGNAL}_{entry_id}"


def json2message(json_message):
    return Message(
        name=json_message.get("name"),
        service=json_message["service"],
        data=json_message["data"],
        created=json_message.get("created"),
        code=json_message.get("code"),
        expires=json_message.get("expires"),
    )


def json_messages_to_list(json_messages):
    messages = []
    for json_message in json_messages:
        messages.append(json2message(json_message))

    return messages


def json_messages_to_dict(json_messages):
    messages = {}
    for json_message in json_messages:
        message = json2message(json_message)
        messages[message.code] = message

    return messages
