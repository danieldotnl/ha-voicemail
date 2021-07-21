from datetime import datetime


class Message:
    def __init__(self, **kwargs):
        self.name = kwargs["name"]
        self.service = kwargs["service"]
        self.data = kwargs["data"]
        self.uid = kwargs["uid"]
        self.expires = kwargs["expires"]
        self.created = kwargs["created"] if kwargs["created"] else datetime.now()
