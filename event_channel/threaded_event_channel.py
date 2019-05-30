import threading

from .event_channel import EventChannel


class ThreadedEventChannel(EventChannel):
    def __init__(self):
        super(ThreadedEventChannel, self).__init__()

    def publish(self, event, *args, **kwargs):
        threads = []
        if event in self.subscribers.keys():
            for callback in self.subscribers[event]:
                threads.append(threading.Thread(
                  target=callback,
                  args=args,
                  kwargs=kwargs
                ))

                for th in threads:
                    th.start()

                for th in threads:
                    th.join()

channel = ThreadedEventChannel()
