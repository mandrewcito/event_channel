import asyncio
import unittest

from event_channel.aio import AsyncEventChannel


def async_test(f):
    def wrapper(*args, **kwargs):
        future = f(*args, **kwargs)
        loop = asyncio.new_event_loop()
        loop.run_until_complete(future)
    return wrapper


class TestEventChannel(unittest.TestCase):
    def setUp(self):
        self.channel = AsyncEventChannel()
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

    @async_test
    async def test_publish(self):
        evt = "myevent"
        func = self.aux_func
        self.channel.subscribe(evt, func)
        self.assertIn(func, self.channel.subscribers[evt])
        await self.channel.publish(evt, 345)
        self.assertEqual(self.myvalue, 345)
        self.channel.unsubscribe(evt, func)
        self.assertNotIn(func, self.channel.subscribers[evt])

    @async_test
    async def test_publish_return(self):
        evt = "myevent"
        func = lambda x: x + 3
        self.channel.subscribe(evt, func)
        value = await self.channel.publish(evt, 345)
        self.assertEqual(value, 345 + 3)
        self.channel.unsubscribe(evt, func)

    @async_test
    async def test_publish_return_list(self):
        evt = "myevent"
        func = lambda x: x + 3
        func2 = lambda x: x + 4
        self.channel.subscribe(evt, func)
        self.channel.subscribe(evt, func2)
        values = await self.channel.publish(evt, 345)
        self.assertEqual(len(values), 2)
        self.assertIn(345 + 3, values)
        self.assertIn(345 + 4, values)
        self.channel.unsubscribe(evt, func)
        self.channel.unsubscribe(evt, func2)

    @async_test
    async def test_publish_multi(self):
        evt = "myevent"
        func = self.multi_aux_func
        self.channel.subscribe(evt, func)
        self.assertIn(func, self.channel.subscribers[evt])
        await self.channel.publish(evt, 345, "asf", 333)
        self.assertEqual(self.myvalue_x, 345)
        self.assertEqual(self.myvalue_y, "asf")
        self.assertEqual(self.myvalue_z, 333)
        self.channel.unsubscribe(evt, func)
        self.assertNotIn(func, self.channel.subscribers[evt])