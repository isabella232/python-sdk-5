import unittest

from configcatclient import ConfigCatClientException
from configcatclient.configcatclient import ConfigCatClient
from configcatclienttests.mocks import ConfigCacheMock, TEST_OBJECT


class ConfigCatClientTests(unittest.TestCase):
    def test_without_project_secret(self):
        with self.assertRaises(ConfigCatClientException):
            ConfigCatClient(None)

    def test_bool(self):
        client = ConfigCatClient('test', 0, 0, None, 0, config_cache_class=ConfigCacheMock)
        self.assertEqual(True, client.get_value('testBoolKey', False))
        client.stop()

    def test_string(self):
        client = ConfigCatClient('test', 0, 0, None, 0, config_cache_class=ConfigCacheMock)
        self.assertEqual('testValue', client.get_value('testStringKey', 'default'))
        client.stop()

    def test_int(self):
        client = ConfigCatClient('test', 0, 0, None, 0, config_cache_class=ConfigCacheMock)
        self.assertEqual(1, client.get_value('testIntKey', 0))
        client.stop()

    def test_double(self):
        client = ConfigCatClient('test', 0, 0, None, 0, config_cache_class=ConfigCacheMock)
        self.assertEqual(1.1, client.get_value('testDoubleKey', 0.0))
        client.stop()

    def test_unknown(self):
        client = ConfigCatClient('test', 0, 0, None, 0, config_cache_class=ConfigCacheMock)
        self.assertEqual('default', client.get_value('testUnknownKey', 'default'))
        client.stop()

    def testInvalidation(self):
        client = ConfigCatClient('test', 0, 0, None, 0, config_cache_class=ConfigCacheMock)
        self.assertEqual(True, client.get_value('testBoolKey', False))
        client.stop()

    def test_config_json(self):
        client = ConfigCatClient('test', 0, 0, None, 0, config_cache_class=ConfigCacheMock)
        self.assertEqual(TEST_OBJECT, client.get_configuration_json())
        client.stop()


if __name__ == '__main__':
    unittest.main()