class EventQueue:
    """A queue of events used to manage things.

    Each item is a tuple.
        (type, info, (data))"""

    queue = []

    def __init__(self):
        """Initialize the queue."""
        queue = [];

    def addToQueue(self, type, info, dataTuple = None):
        """Add an item to the end of the queue."""
        tuple = (type, info, dataTuple)
        self.queue.append(tuple)

    def addToQueueFront(self, type, info, dataTuple = None):
        """Add an item to the front of the queue."""
        tuple = (type, info, dataTuple)
        self.queue.insert(0, tuple)

    def getFromQueue(self):
        """Get the item at the front of the queue."""
        return self.queue.pop(0)

    def emptyQueue(self):
        """Empty the queue."""
        self.queue = [];

    def isEmpty(self):
        """Is the queue empty? Yes or no!"""
        if (len(self.queue) == 0):
            return 1
        else:
            return 0
