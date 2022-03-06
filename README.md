# Event Channel
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg?logo=paypal&style=flat-square)](https://www.paypal.me/mandrewcito/1)&nbsp;
![Pypi](https://img.shields.io/pypi/v/event_channel.svg)
[![Downloads](https://pepy.tech/badge/event-channel)](https://pepy.tech/project/event-channel)
[![Downloads](https://pepy.tech/badge/event-channel/month)](https://pepy.tech/project/event-channel/month)
![Travis ci](https://img.shields.io/travis/mandrewcito/event_channel.svg)
![Issues](https://img.shields.io/github/issues/mandrewcito/event_channel.svg)
![Open issues](https://img.shields.io/github/issues-raw/mandrewcito/event_channel.svg)
![codecov.io](https://codecov.io/github/mandrewcito/event_channel/coverage.svg?branch=master)

Another library with a pub/sub implementation. You can subscribe functions to a certain topic (aka event). When a message is sent through this event callback functions subscribed will be executed.

```python
from event_channel import EventChannel

mychannel = EventChannel() # You can also import channel, is an instance already created

def callback(x):
    x = x + 1
    print(x)

mychannel.subscribe("myevent", callback)

mychannel.publish("myevent", 345)

channel.unsubscribe("myevent", callback)
```


```python

from event_channel.threaded_event_channel import ThreadedEventChannel

mychannel =  ThreadedEventChannel(blocking=False) # You can also import non_blocking_channel, is an instance already created

def callback(x):
    x = x + 1
    print(x)

mychannel.subscribe("myevent", callback)
mychannel.subscribe("myevent", callback2)

threads = mychannel.publish("myevent", 345)

# Wait thread finish
for thread in threads:
    thread.join()
```

```python

from event_channel.threaded_event_channel import ThreadedEventChannel

my_blocking_channel = ThreadedEventChannel() # You can also import channel, is an instance already created

def callback(x):
    x = x + 1
    print(x)

mychannel.subscribe("myevent", callback)
mychannel.subscribe("myevent", callback2)

threads = mychannel.publish("myevent", 345)
#at this point all threads are finished

```