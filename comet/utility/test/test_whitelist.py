# Comet VOEvent Broker.
# Test for IP whitelisting system.

from ipaddress import ip_network

from twisted.internet.protocol import ServerFactory
from twisted.internet.protocol import Protocol
from twisted.internet.address import IPv4Address, UNIXAddress
from twisted.python import log as twisted_log
from twisted.trial import unittest

from comet.utility import WhitelistingFactory
from comet.testutils import DummyLogObserver


class TestFactory(ServerFactory):
    protocol = Protocol
    test_attribute = "test_attribute"


class WhitelistingFactoryTestCase(unittest.TestCase):
    def setUp(self):
        self.observer = DummyLogObserver()
        twisted_log.addObserver(self.observer)

    def tearDown(self):
        twisted_log.removeObserver(self.observer)

    def test_empty_whitelist(self):
        # All connections should be denied and a default message logged.
        factory = WhitelistingFactory(TestFactory(), [])
        self.assertEqual(
            factory.buildProtocol(IPv4Address("TCP", "127.0.0.1", 0)), None
        )
        self.assertEqual(len(self.observer.messages), 1)
        self.assertTrue("connection" in self.observer.messages[0][0])

    def test_in_whitelist(self):
        # Connection should be accepted and nothing logged.
        factory = WhitelistingFactory(TestFactory(), [ip_network("0.0.0.0/0")])
        self.assertIsInstance(
            factory.buildProtocol(IPv4Address("TCP", "127.0.0.1", 0)), Protocol
        )
        self.assertEqual(len(self.observer.messages), 0)

    def test_not_in_whitelist(self):
        # Connection should be accepted and nothing logged.
        factory = WhitelistingFactory(TestFactory(), [ip_network("127.0.0.1/32")])
        self.assertEqual(
            factory.buildProtocol(IPv4Address("TCP", "127.0.0.2", 0)), None
        )

    def test_log_message(self):
        # Should be possible to customize the message which is logged.
        TEST_STRING = "test-1234"
        factory = WhitelistingFactory(
            TestFactory(), [ip_network("127.0.0.1/32")], TEST_STRING
        )
        self.assertEqual(
            factory.buildProtocol(IPv4Address("TCP", "127.0.0.2", 0)), None
        )
        self.assertFalse("connection" in self.observer.messages[0][0])
        self.assertTrue(TEST_STRING in self.observer.messages[0][0])

    def test_getattr_delegation(self):
        """Check that missing attributes are delegated to the wrapped factory."""
        factory = WhitelistingFactory(TestFactory(), [])

        # This attribute is defined on the wrapped factory.
        self.assertEqual(factory.test_attribute, TestFactory.test_attribute)

        with self.assertRaises(AttributeError):
            # This attribute does not exist.
            factory.bad_attribute

    def test_unix_domain_socket(self):
        """Test that the whitelist is skipped for Unix domain sockets."""
        factory = WhitelistingFactory(TestFactory(), [])

        # Should be blocking IP addresses
        self.assertEqual(
            factory.buildProtocol(IPv4Address("TCP", "127.0.0.1", 0)), None
        )

        # But Unix domain sockets are allowed
        self.assertIsInstance(
            factory.buildProtocol(UNIXAddress("/test/address")), Protocol
        )

        # With a warning logged
        self.assertTrue("Bypassing" in self.observer.messages[1][0])
