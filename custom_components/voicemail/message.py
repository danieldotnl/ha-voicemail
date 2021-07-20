from datetime import datetime


class Message:
    def __init__(self, name, service, data):
        self.name = name
        self.service = service
        self.data = data
        self.created = datetime.now()
