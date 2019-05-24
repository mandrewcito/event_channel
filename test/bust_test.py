from comm_bus.bus import bus_instance
ff = lambda x: print(x)
bus_instance.subscribe("myevent", ff)


bus_instance.publish("myevent", "Hello, world!")

bus_instance.unsubscribe("myevent", ff)

bus_instance.publish("myevent", "Hello, world!")