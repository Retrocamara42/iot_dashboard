# Python imports
import json, os
from uuid import uuid4
import pytz
from datetime import datetime, timedelta
# Channels import
from channels.generic.websocket import WebsocketConsumer
# Django imports
from django.core import serializers
# Aws imports
from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
# Project imports
from .models import *
from iot_dashboard.constants import *

utc_5 = pytz.timezone('America/Lima')
DATA_TIME_THRESHOLD = 60 # in days

class EnvMonitorConsumer(WebsocketConsumer):
    ########### Subscription functions ###########
    def on_temp_received(self, topic, payload, **kwargs):
        print("Received message from topic '{}': {}".format(topic, payload))
        message=json.loads(payload.decode('ascii'))
        if(message["dev_name"]==self.device_name):
            self.send(text_data=json.dumps({
                'message': [{
                    'topic':topic,
                    'timestamp':datetime.now(tz=utc_5).strftime("%Y-%m-%d %H:%M:%S"),
                    'temp':message['temp']
                }]
            }))

    def on_humid_received(self, topic, payload, **kwargs):
        print("Received message from topic '{}': {}".format(topic, payload))
        message=json.loads(payload.decode('ascii'))
        if(message["dev_name"]==self.device_name):
            self.send(text_data=json.dumps({
                'message': [{
                    'topic':topic,
                    'timestamp':datetime.now(tz=utc_5).strftime("%Y-%m-%d %H:%M:%S"),
                    'humid':message["humid"]
                }]
            }))

    def on_pressure_received(self, topic, payload, **kwargs):
        print("Received message from topic '{}': {}".format(topic, payload))
        message=json.loads(payload.decode('ascii'))
        if(message["dev_name"]==self.device_name):
            self.send(text_data=json.dumps({
                'message': [{
                    'topic':topic,
                    'timestamp':datetime.now(tz=utc_5).strftime("%Y-%m-%d %H:%M:%S"),
                    'press':message["pressure"]
                }]
            }))

    ########### Database functions ###########
    """
    get_temperature_data: Gets temperature data
    """
    def get_temperature_data(self, max_points):
        # can't show data that is too far apart
        latest_timestamp = Temperature.objects.latest('timestamp').timestamp
        threshold_date = latest_timestamp - timedelta(days=DATA_TIME_THRESHOLD)
        dataset = Temperature.objects.filter(timestamp__gte=threshold_date
                    ).order_by('-id')[:max_points]
        return serializers.serialize('json', dataset)

    """
    get_humidity_data: Gets humidity data
    """
    def get_humidity_data(self, max_points):
        latest_timestamp = Temperature.objects.latest('timestamp').timestamp
        threshold_date = latest_timestamp - timedelta(days=DATA_TIME_THRESHOLD)
        dataset = Humidity.objects.filter(timestamp__gte=threshold_date
                    ).order_by('-id')[:max_points]
        return serializers.serialize('json', dataset)

    """
    get_pressure_data: Gets pressure data
    """
    def get_pressure_data(self, max_points):
        latest_timestamp = Temperature.objects.latest('timestamp').timestamp
        threshold_date = latest_timestamp - timedelta(days=DATA_TIME_THRESHOLD)
        dataset = Pressure.objects.filter(timestamp__gte=threshold_date
                    ).order_by('-id')[:max_points]
        return serializers.serialize('json', dataset)
    

    ########### Consumer functions ###########
    def connect(self):
        self.device_name = self.scope['url_route']['kwargs']['device_name']
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

        subscribe_temp, packet_id_t = self.mqtt_connection.subscribe(
                topic="temperature",
                qos=mqtt.QoS.AT_LEAST_ONCE,
                callback=self.on_temp_received)
        subscribe_result = subscribe_temp.result()
        print("Subscribed with {}".format(str(subscribe_result['qos'])))

        subscribe_humid, packet_id_h = self.mqtt_connection.subscribe(
                topic="humidity",
                qos=mqtt.QoS.AT_LEAST_ONCE,
                callback=self.on_humid_received)
        subscribe_result = subscribe_humid.result()
        print("Subscribed with {}".format(str(subscribe_result['qos'])))

        subscribe_press, packet_id_p = self.mqtt_connection.subscribe(
                topic="pressure",
                qos=mqtt.QoS.AT_LEAST_ONCE,
                callback=self.on_pressure_received)
        subscribe_result = subscribe_press.result()
        print("Subscribed with {}".format(str(subscribe_result['qos'])))


    def disconnect(self, close_code):
        disconnect_future = self.mqtt_connection.disconnect()
        disconnect_future.result()


    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        if(message['command']=='send_initial_data_temp'):
            try:
                max_points=int(message['max_points'])
                if(max_points<=0 or max_points>999):
                    max_points=20
            except Exception as e:
                max_points=20
                print("Error while converting max_points to int: "+str(e))
            # Sending all events from database
            temp_data=self.get_temperature_data(max_points)
            self.send(text_data=json.dumps({
                'message': temp_data
            }))
        elif(message['command']=='send_initial_data_humid'):
            try:
                max_points=int(message['max_points'])
                if(max_points<=0 or max_points>999):
                    max_points=20
            except Exception as e:
                max_points=20
                print("Error while converting max_points to int: "+str(e))
            # Sending all events from database
            humid_data=self.get_humidity_data(max_points)
            self.send(text_data=json.dumps({
                'message': humid_data
            }))
        elif(message['command']=='send_initial_data_press'):
            try:
                max_points=int(message['max_points'])
                if(max_points<=0 or max_points>999):
                    max_points=20
            except Exception as e:
                max_points=20
                print("Error while converting max_points to int: "+str(e))
            # Sending all events from database
            press_data=self.get_pressure_data(max_points)
            self.send(text_data=json.dumps({
                'message': press_data
            }))
        elif(message['command']=='query_device'):
            self.mqtt_connection.publish(
                topic='remote_action',
                payload=json.dumps({"q":1}),
                qos=mqtt.QoS.AT_LEAST_ONCE)
            self.send(text_data=json.dumps({
                'message': [{
                    'command_response': 'Mensaje de consulta enviado'
                }]
            }))
        elif(message['command']=='set_frequency'):
            freq=message['freq']
            try:
                freq=int(freq)
            except Exception as e:
                print("Error while parsing value frequency to int: "+str(e))
                freq=-1
            if(freq>0 and freq<=999):
                resp=self.mqtt_connection.publish(
                    topic='remote_action',
                    payload=json.dumps({"f":freq}),
                    qos=mqtt.QoS.AT_LEAST_ONCE)
                print(resp)
                self.send(text_data=json.dumps({
                    'message': [{
                        'command_response': 'Mensaje para actualizar frecuencia enviado'
                        }]
                }))
