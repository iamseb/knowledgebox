import uuid

class GUIDObject(object):
    def __init__(self, *args, **kwargs):
        self.guid = uuid.uuid4()
