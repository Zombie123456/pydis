import time
from unittest import TestCase

from pydis import Pydis
from pydis.exceptions import NotFound


class TestCore(TestCase):
    def test_set_get(self):
        p = Pydis()
        fake_key, fake_value = 'fake_key', 'fake_value'
        p.set(fake_key, fake_value)
        ret = p.get(fake_key)
        self.assertEqual(ret, fake_value)

    def test_ttl(self):
        p = Pydis()
        fake_key, fake_value = 'timeout_key', 'timeout_value'
        p.set(fake_key, fake_value, timeout=2)
        self.assertEqual(p.get(fake_key), fake_value)
        self.assertIs(p.ttl(fake_key) > 0, True)
        time.sleep(2)
        self.assertIsNone(p.get(fake_key))

    def test_nx(self):
        p = Pydis()
        fake_key, fake_value = 'nx_key', 'nx_value'
        p.set_nx(fake_key, fake_value)
        self.assertEqual(p.get(fake_key), fake_value)
        p.set_nx(fake_key, "new_value")
        self.assertEqual(p.get(fake_key), fake_value)

    def test_delete(self):
        p = Pydis()
        fake_key, fake_value = 'delete_key', 'delete_value'
        p.set(fake_key, fake_value)
        p.delete(fake_key)
        self.assertIsNone(p.get(fake_key))

    def test_incr(self):
        p = Pydis()
        fake_key = 'incr_key'
        p.set(fake_key, 0)
        p.incr(fake_key)
        self.assertEqual(p.get(fake_key), 1)

        p.incr(fake_key, 2)
        self.assertEqual(p.get(fake_key), 3)

        with self.assertRaises(NotFound):
            p.incr('dose not exists key')

    def test_decr(self):
        p = Pydis()
        fake_key = 'decr_key'
        p.set(fake_key, 3)
        p.decr(fake_key)
        self.assertEqual(p.get(fake_key), 2)

        p.decr(fake_key, 2)
        self.assertEqual(p.get(fake_key), 0)

        with self.assertRaises(NotFound):
            p.incr('dose not exists key')

    def test_keys(self):
        p = Pydis()
        p.force_clean()
        keys = ['e', 'a', 'b', 'c', 'd']
        for index, key in enumerate(keys, 1):
            p.set(key, 1, index)

        time.sleep(2)
        self.assertListEqual(['b', 'c', 'd'], p.keys())

    def test_clean(self):
        p = Pydis()
        p.set('a', 1, 1)
        p.set('b', 2)

        time.sleep(1)
        p.clean()
        with self.assertRaises(NotFound):
            _ = p._data['a']
        self.assertEqual(p.get('b'), 2)

    def test_force_clean(self):
        p = Pydis()
        keys = ['e', 'a', 'b', 'c', 'd']
        for key in keys:
            p.set(key, 1)
        p.force_clean()
        self.assertListEqual([], p.keys())

    def test_len(self):
        p = Pydis()
        p.force_clean()
        self.assertEqual(len(p), 0)
