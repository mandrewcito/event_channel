import logging


class EventChannel(object):
    def __init__(self):
        logger = logging.getLogger(__name__)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
                '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.WARNING)
        self._log = logger
        self.subscribers = {}

    def unsubscribe(self, event, callback):
        if event is not None or event != ""\
                and event in self.subscribers.keys():
            self.subscribers[event] = list(
                filter(
                    lambda x: x is not callback,
                    self.subscribers[event]
                )
            )
        else:
            self._log.warning(
                "Cant unsubscribe function '{0}' from event '{1}' ".format(
                    event,
                    callback))

    def subscribe(self, event, callback):
        if not callable(callback):
            raise ValueError("callback must be callable")

        if event is None or event == "":
            raise ValueError("Event cant be empty")

        if event not in self.subscribers.keys():
            self.subscribers[event] = [callback]
        else:
            self.subscribers[event].append(callback)

    def publish(self, event, *args, **kwargs):
        if event in self.subscribers.keys():
            for callback in self.subscribers[event]:
                callback(*args, **kwargs)
        else:
            self._log.warning("Event {0} has no subscribers".format(event))

channel = EventChannel()
