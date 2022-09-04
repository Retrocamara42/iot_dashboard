import json, os
from uuid import uuid4
import pytz
from datetime import datetime
# Channels import
from channels.generic.websocket import WebsocketConsumer
# Aws imports
from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
# Project imports
from .models import *
from environment_monitor.models import *
from iot_dashboard.constants import *
from django.conf import settings

utc_5 = pytz.timezone('America/Lima')

class AniM5StackConsumer(WebsocketConsumer):
    ########### Subscription functions ###########
    def on_sd_info_received(self, topic, payload, **kwargs):
        print("Received message from topic '{}': {}".format(topic, payload))
        message=json.loads(payload.decode('ascii'))
        if(message["dev_name"]==self.device_name):
            if(topic=="m5_sd_info"):
                self.send(text_data=json.dumps({
                    'message': [{
                        'topic':topic,
                        'total_storage':message['total_storage'],
                        'free_storage':message['free_storage'],
                        'used_storage':message['used_storage']
                    }]
                }))
            elif(topic=="m5_alive"):
                self.send(text_data=json.dumps({
                    'message': [{
                        'topic':topic,
                        'total_storage':message['total_storage'],
                        'free_storage':message['free_storage'],
                        'used_storage':message['used_storage']
                    }]
                }))


    ########### Consumer functions ###########
    def connect(self):
        self.device_name = self.scope['url_route']['kwargs']['device_name']
        print("Connected to device:",self.device_name)
        self.accept()
        # Creating event loop
        self.event_loop_group = io.EventLoopGroup(1)
        host_resolver = io.DefaultHostResolver(self.event_loop_group)
        client_bootstrap = io.ClientBootstrap(self.event_loop_group, host_resolver)
        self.mqtt_connection = mqtt_connection_builder.mtls_from_path(
                endpoint=os.getenv('MQTT_ENDPOINT'),
                port=int(os.getenv('MQTT_PORT')),
                cert_filepath=CERT_FILEPATH,
                pri_key_filepath=PRI_KEY_FILEPATH,
                ca_filepath=CA_FILEPATH,
                client_bootstrap=client_bootstrap,
                clean_session=False,
                client_id="iot-" + str(uuid4()),
                keep_alive_secs=6,)
        connect_future = self.mqtt_connection.connect()
        connect_future.result()

        subscribe_sd_info, packet_id_t = self.mqtt_connection.subscribe(
                topic="m5_sd_info",
                qos=mqtt.QoS.AT_LEAST_ONCE,
                callback=self.on_sd_info_received)
        subscribe_result = subscribe_sd_info.result()
        print("Subscribed with {}".format(str(subscribe_result['qos'])))


    def disconnect(self, close_code):
        disconnect_future = self.mqtt_connection.disconnect()
        disconnect_future.result()


    def receive(self, text_data=None, bytes_data=None):
        pass