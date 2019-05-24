import unittest

from event_channel.event_channel import EventChannel

class TestStringMethods(unittest.TestCase):
    def setUp(self):
        self.channel = EventChannel()

    def tearDown(self):
        pass

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

    def test_unsubscribe(self):
        ff = lambda x: print(x)
        self.channel.subscribe("myevent", ff)
        self.assertIn(ff, self.channel.subscribers["myevent"])
        self.channel.unsubscribe("myevent", ff)
        self.assertNotIn(ff, self.channel.subscribers["myevent"])