import unittest

from event_channel.event_channel import EventChannel


class TestEventChannel(unittest.TestCase):
    def setUp(self):
        self.channel = EventChannel()
        self.myvalue = None
        self.myvalue_x = None
        self.myvalue_y = None
        self.myvalue_z = None

    def tearDown(self):
        self.myvalue = None
        self.myvalue_x = None
        self.myvalue_y = None
        self.myvalue_z = None

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_subscribe(self):
        ff = lambda x: x + 1
        self.channel.subscribe("myevent", ff)
        self.assertIn(ff, self.channel.subscribers["myevent"])
        self.channel.unsubscribe("myevent", ff)
        self.assertNotIn(ff, self.channel.subscribers["myevent"])

    def test_unsubscribe(self):
        ff = lambda x: x + 1
        self.channel.subscribe("myevent", ff)
        self.assertIn(ff, self.channel.subscribers["myevent"])
        self.channel.unsubscribe("myevent", ff)
        self.assertNotIn(ff, self.channel.subscribers["myevent"])

    def aux_func(self, x):
        self.myvalue = x

    def multi_aux_func(self, x, y, z):
        self.myvalue_x = x
        self.myvalue_y = y
        self.myvalue_z = z

    def test_publish(self):
        evt = "myevent"
        func = self.aux_func
        self.channel.subscribe(evt, func)
        self.assertIn(func, self.channel.subscribers[evt])
        self.channel.publish(evt, 345)
        self.assertEqual(self.myvalue, 345)
        self.channel.unsubscribe(evt, func)
        self.assertNotIn(func, self.channel.subscribers[evt])

    def test_publish_multi(self):
        evt = "myevent"
        func = self.multi_aux_func
        self.channel.subscribe(evt, func)
        self.assertIn(func, self.channel.subscribers[evt])
        self.channel.publish(evt, 345, "asf", 333)
        self.assertEqual(self.myvalue_x, 345)
        self.assertEqual(self.myvalue_y, "asf")
        self.assertEqual(self.myvalue_z, 333)
        self.channel.unsubscribe(evt, func)
        self.assertNotIn(func, self.channel.subscribers[evt])