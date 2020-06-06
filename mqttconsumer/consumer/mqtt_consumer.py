# -*- coding: UTF-8 -*-

# --*-- built-in packages --*--
import json
import os
import socket
import time
import traceback
import logging
from json import dumps
from datetime import datetime, timedelta
import random

# --*-- Installed packages --*--
import paho.mqtt.client as mqtt
import requests
import psutil

# --*-- own packages --*--
from create_log import create_log


from data.beacon import beacon
from data.freecon import freecon
from repository.data import save_one


class MQTTConsumer(mqtt.Client):
    def __init__(self,
            TOPIC_DATA = os.getenv('TOPIC_DATA'),
            TOPIC_MONITORING = os.getenv('TOPIC_MONITORING'),
            BROKER_HOST = os.getenv('BROKER_HOST'),
            BROKER_PORT = os.getenv('BROKER_PORT'),
            USER_MQTT = os.getenv('USER_MQTT'),
            PASS_MQTT = os.getenv('PASS_MQTT'),
            CLIENT_ID=os.getenv('CLIENT_ID', ''),
            logger = logging.getLogger(),
            *args):
        super(MQTTConsumer, self).__init__(*args)
        self.TOPIC_DATA = TOPIC_DATA
        self.TOPIC_MONITORING = TOPIC_MONITORING
        self.BROKER_HOST = BROKER_HOST
        self.BROKER_PORT = int(BROKER_PORT)
        self.USER_MQTT = USER_MQTT
        self.PASS_MQTT = PASS_MQTT
        self.logger = logger

    def on_connect(self, client, userdata, flags, rc):
        '''The callback for when the client receives a CONNACK response from
        the server.
        '''
        # Subscribing in on_connect() means that if we lose the
        # connection and reconnect then subscriptions will be renewed.
        if rc == 0:
            self.logger.info('MQTT connection successful!')
            subscriptions = [
                ('IoT/mapper/#', 2)
            ]
            client.subscribe(subscriptions)
        else:
            self.logger.warning(f'Bad connection returned code: {rc}')

    def on_subscribe(self, client, userdata, mid, granted_qos):
        self.logger.info('Subscribe to topic successful!')

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            self.logger.warning(f'Unexpected disconnection. rc: {rc}')

    def on_message(self, client, userdata, msg):
        # The callback for when a PUBLISH message is received from the server
        try:
            payload_str = msg.payload.decode('utf-8')
        except UnicodeDecodeError as error:
            self.logger.exception(f'Decoding payload: {error}')
            return

        try:
            mqtt_payload = json.loads(payload_str)
        except json.decoder.JSONDecodeError as error:
            self.logger.exception(f'Loading payload: {error}')
            return

        topic = msg.topic
        self.logger.info(f'topic: {topic}')
        self.logger.info(f'payload: {mqtt_payload}')

        try:
            beacon_for_search = topic.split("/")[3]
            beacon_found = beacon[beacon_for_search]
            freecon_found = freecon[str(mqtt_payload['freecon'])]
            measurement_type = topic.split("/")[2]
            time = mqtt_payload['now']
            tags = {
                'beacon': beacon_for_search,
                'freecon': mqtt_payload['freecon']
            }
            fields = {
                'room': beacon_found['room'],
                'building': beacon_found['building'],
                'client': beacon_found['client'],
                'user': freecon_found['user']['code'],
                'age': freecon_found['user']['age'],
                'height': freecon_found['user']['height'],
                'education': freecon_found['user']['education'],
                'x_position' = mqtt_payload['x_position'],
                'y_position' = mqtt_payload['y_position'],
                'z_position' = mqtt_payload['z_position']
            }

            self.logger.info(f'time: {time}')
            self.logger.info(f'measurement: {measurement_type}')
            self.logger.info(f'tags: {tags}')

            save_one(
                time = time,
                measurement = measurement_type,
                tags = tags,
                fields = fields
            )
        except Exception as eption:
            import traceback
            traceback.print_exc()

    def connect_system(self):
        broker_host = self.BROKER_HOST
        broker_port = self.BROKER_PORT
        self.username_pw_set(self.USER_MQTT, password=self.PASS_MQTT)
        self.connect_async(broker_host, port=broker_port, keepalive=60,
            bind_address="")
        self.loop_start()
        while True:
            time.sleep(1)

def main():
    logger = create_log(log_name="mqtt_consumer")
    client = MQTTConsumer(logger = logger)
    client.connect_system()

if __name__ == '__main__':
    main()
