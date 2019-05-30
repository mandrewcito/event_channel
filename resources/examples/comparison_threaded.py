import time
from event_channel.event_channel import EventChannel
from event_channel.threaded_event_channel import ThreadedEventChannel

non_thread = EventChannel()
threaded = ThreadedEventChannel()

non_thread.subscribe("myevent", time.sleep)
non_thread.subscribe("myevent", time.sleep)
start = time.time()
non_thread.publish("myevent", 3)
end = time.time()
print("non threaded function elapsed time {0}".format(end - start))
#non threaded function elapsed time 6.0080871582
threaded.subscribe("myevent", time.sleep)
threaded.subscribe("myevent", time.sleep)
start = time.time()
threaded.publish("myevent", 3)
end = time.time()
print("threaded function elapsed time {0}".format(end - start))
# threaded function elapsed time 3.00581121445