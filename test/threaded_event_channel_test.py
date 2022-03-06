import unittest
import time

from event_channel.threaded_event_channel import ThreadedEventChannel


class TestThreadedEventChannel(unittest.TestCase):
    def setUp(self):
        self.channel = ThreadedEventChannel()
        self.non_blocking_channel = ThreadedEventChannel(blocking=False)
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

    def test_subscribe_fail_event(self):
        self.assertRaises(
            ValueError,
            self.channel.subscribe,
            "",
            lambda x: x + 1)
            
    def test_subscribe_fail_function(self):
        self.assertRaises(
            ValueError,
            self.channel.subscribe,
            "myevent",
            13)

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
        time.sleep(4)

    def multi_aux_func(self, x, y, z):
        time.sleep(2)
        self.myvalue_x = x
        self.myvalue_y = y
        self.myvalue_z = z


    def test_publish(self):
        evt = "myevent"
        func = self.aux_func
        func2 = self.aux_func
        self.channel.subscribe(evt, func)
        self.channel.subscribe(evt, func2)
        self.assertIn(func, self.channel.subscribers[evt])
        self.assertIn(func2, self.channel.subscribers[evt])
        self.channel.publish(evt, 345)
        self.assertEqual(self.myvalue, 345)
        self.channel.unsubscribe(evt, func)
        self.channel.unsubscribe(evt, func2)
        self.assertNotIn(func, self.channel.subscribers[evt])
        self.assertNotIn(func2, self.channel.subscribers[evt])

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

    def test_non_blocking(self):
        evt = "myevent"
        func = self.multi_aux_func
        x, y, z = self.myvalue_x, self.myvalue_y, self.myvalue_z
        self.non_blocking_channel.subscribe(evt, func)
        self.assertIn(func, self.non_blocking_channel.subscribers[evt])
        threads = self.non_blocking_channel.publish(evt, 345, "asf", 333)
        
        self.assertEquals(len(threads), len(self.non_blocking_channel.subscribers[evt]))
        self.assertEqual(self.myvalue_x, x)
        self.assertEqual(self.myvalue_y, y)
        self.assertEqual(self.myvalue_z, z)
                
        for thread in threads:
            thread.join()

        self.assertEqual(self.myvalue_x, 345)
        self.assertEqual(self.myvalue_y, "asf")
        self.assertEqual(self.myvalue_z, 333)
        self.non_blocking_channel.unsubscribe(evt, func)
        self.assertNotIn(func, self.non_blocking_channel.subscribers[evt])
