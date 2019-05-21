#_*_ coding: utf-8 _*_


import unittest
from MyDict import Dict

class TestDict(unittest.TestCase):

    def setUp(self):
        print('setup...')

    def tearDown(self):
        print('tearDown...')

    def test_init(self):
        d = Dict(a=1, b='2')
        self.assertEquals(d.a,1)
        self.assertEquals(d.b,'2')
        self.assertTrue(isinstance(d,dict))

    def test_key(self):
        d = Dict()
        d['key'] = 'value'
        self.assertEquals(d.key, 'value')
        pass

    def test_attr(self):
        d = Dict()
        d.key = 'value'
        self.assertTrue('key' in d)
        self.assertEquals(d['key'], 'value')
        pass

    def test_keyerror(self):
        d = Dict()
        with self.assertRaises(KeyError):
            value = d['key']
            pass

    def test_attrerror(self):
        d = Dict()
        with self.assertRaises(AttributeError):
            value = d.key
            pass



if __name__ == '__main__':
    unittest.main()