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


class MQTTPublisher(mqtt.Client):
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
        super(MQTTPublisher, self).__init__(*args)
        self.TOPIC_DATA = TOPIC_DATA
        self.TOPIC_MONITORING = TOPIC_MONITORING
        self.BROKER_HOST = BROKER_HOST
        self.BROKER_PORT = int(BROKER_PORT)
        self.USER_MQTT = USER_MQTT
        self.PASS_MQTT = PASS_MQTT
        self.logger = logger

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            self.logger.warning(f'Unexpected disconnection. rc: {rc}')

    def connect_system(self):
        broker_host = self.BROKER_HOST
        broker_port = self.BROKER_PORT
        self.username_pw_set(self.USER_MQTT, password=self.PASS_MQTT)
        self.connect_async(broker_host, port=broker_port, keepalive=60,
            bind_address="")
        self.loop_start()


def main():
    logger = create_log(log_name="mqtt_publisher")
    client = MQTTPublisher(logger = logger)
    client.connect_system()
    start_ciclying(client)

def start_ciclying(client):
    #Place n: [freecons, becons]
    places_simulation = {
        '1': [[0, 9], [1000, 1004]], #White House
        '2': [[10, 14], [2000, 2002]], #Jail
        '3': [[15, 19], [3000, 3002]] #Office
    }
    while True:
        place = random.randint(1, len(places_simulation.keys()))
        random_freecon = random.randint(places_simulation[str(place)][0][0], places_simulation[str(place)][0][1])
        random_becon = random.randint(places_simulation[str(place)][1][0], places_simulation[str(place)][1][1])
        random_x = random.randint(0, 255)
        random_y = random.randint(0, 255)
        random_z = random.randint(0, 255)
        msg = dumps({
            'freecon': random_freecon,
            'now': datetime.strftime(datetime.now() + timedelta(hours = 5), '%Y-%m-%dT%H:%M:%SZ'),
            'x_position': random_x,
            'y_position': random_y,
            'z_position': random_z
        })
        random_number = random.randint(1, 10)
        if random_number in [1, 2, 3, 4, 5, 6 ,7]:
            client.publish(topic=f'IoT/mapper/report/{random_becon}',
                payload=msg, qos=0)
        elif random_number in [8, 9]:
            client.publish(topic=f'IoT/mapper/forbidden/{random_becon}',
                payload=msg, qos=1)
        elif random_number in [10]:
            client.publish(topic=f'IoT/mapper/unlock/{random_becon}',
                payload=msg, qos=1)

        time.sleep(1)

if __name__ == '__main__':
    main()
