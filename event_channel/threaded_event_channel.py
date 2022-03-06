import threading

from .event_channel import EventChannel


class ThreadedEventChannel(EventChannel):
    def __init__(self, blocking=True):
        self.blocking = blocking
        super(ThreadedEventChannel, self).__init__()

    def publish(self, event, *args, **kwargs):
        threads = []

        if event not in self.subscribers.keys():
            self._log.warning("Event {0} has no subscribers".format(event))
            return []

        for callback in self.subscribers[event]:
            threads.append(threading.Thread(
                target=callback,
                args=args,
                kwargs=kwargs
            ))

        for th in threads:
            th.start()

        if self.blocking:
            for th in threads:
                th.join()
        return threads

channel = ThreadedEventChannel()

non_blocking_channel = ThreadedEventChannel(blocking=False)
