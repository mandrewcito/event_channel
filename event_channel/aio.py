from .event_channel import EventChannel

class AsyncEventChannel(EventChannel):
    def __init__(self):
        super(AsyncEventChannel, self).__init__()

    async def publish(self, event, *args, **kwargs):
        if event not in self.subscribers.keys():
            self._log.warning("Event {0} has no subscribers".format(event))
            return 
        
        callbacks = self.subscribers[event]

        if len(callbacks) == 0:
            self._log.warning("Event {0} has no subscribers".format(event))
            return
        
        if len(callbacks) == 1:
            return callbacks[0](*args, **kwargs)

        return [
            callback(*args, **kwargs)
            for callback in callbacks]

async_channel = AsyncEventChannel()