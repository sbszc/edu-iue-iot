import os
import unittest
from datetime import datetime

from mqtt_consumer import MQTTConsumer


class TestMQTTConsumer(unittest.TestCase):

    def setUp(self):
        self.mqtt_client = MQTTConsumer()

    def test_good_raw_data_publish(self):
        pass
