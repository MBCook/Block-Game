class EventQueue:
    """A queue of events used to manage things.

    Each item is a tuple.
        (type, info)"""

    queue = []

    def __init__(self):
        queue = [];

    def addToQueue(self, type, info):
        tuple = (type, info)
        self.queue.append(tuple)

    def addToQueueFront(self, type, info):
        tuple = (type, info)
        self.queue.insert(0, tuple)

    def getFromQueue(self):
        return self.queue.pop(0)

    def emptyQueue(self):
        self.queue = [];

    def isEmpty(self):
        if (len(self.queue) == 0):
            return 1
        else:
            return 0
