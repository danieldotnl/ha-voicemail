import uuid
from datetime import datetime


class Message:
    def __init__(self, **kwargs):
        self.name = kwargs["name"]
        self.service = kwargs["service"]
        self.data = kwargs["data"]
        if kwargs["code"]:
            self.code = kwargs["code"]
        else:
            self.code = uuid.uuid4().hex
        self.expires = kwargs["expires"]
        self.created = kwargs["created"] if kwargs["created"] else datetime.now()
