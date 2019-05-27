import unittest

from event_channel.event_channel import EventChannel


class TestStringMethods(unittest.TestCase):
    def setUp(self):
        self.channel = EventChannel()
        self.myvalue = None

    def tearDown(self):
        self.myvalue = None

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_subscribe(self):
        ff = lambda x: print(x)
        self.channel.subscribe("myevent", ff)
        self.assertIn(ff, self.channel.subscribers["myevent"])
        self.channel.unsubscribe("myevent", ff)
        self.assertNotIn(ff, self.channel.subscribers["myevent"])

    def test_unsubscribe(self):
        ff = lambda x: print(x)
        self.channel.subscribe("myevent", ff)
        self.assertIn(ff, self.channel.subscribers["myevent"])
        self.channel.unsubscribe("myevent", ff)
        self.assertNotIn(ff, self.channel.subscribers["myevent"])

    def aux_func(self, x):
        self.myvalue = x

    def test_publish(self):
        evt = "myevent"
        func = self.aux_func
        self.channel.subscribe(evt, func)
        self.assertIn(func, self.channel.subscribers[evt])
        self.channel.publish(evt, 345)
        self.assertEqual(self.myvalue, 345)
        self.channel.unsubscribe(evt, func)
        self.assertNotIn(func, self.channel.subscribers[evt])