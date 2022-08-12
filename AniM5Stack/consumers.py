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
from iot_dashboard.constants import *
import binascii
from django.conf import settings

utc_5 = pytz.timezone('America/Lima')

class AniM5StackConsumer(WebsocketConsumer):
    PACKET_SIZE=384
    ACCEPT_STREAM_TOPIC="$aws/things/anim5stack/streams/StreamId/description/json"
    REJECT_STERAM_TOPIC="$aws/things/anim5stack/streams/StreamId/rejected/json"

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
            elif(topic=="sd_missing_file"):
                print("SD missing files")
                missing_files=message['miss_files'].split(";")
                path_file=settings.MEDIA_ROOT+missing_file
                num_packets = 1+os.path.getsize(path_file)/self.PACKET_SIZE
                missing_files=missing_files[1:]
                print(missing_files)
                ranges=[]
                for missing_file in missing_files[1:]:
                    # Get ranges
                    delimiters=missing_file.split("_")
                    print("Delimiters found: "+str(delimiters))
                    if len(delimiters)==1:
                        ranges.append(delimiters[0])
                    else:
                        ranges.append((delimiters[0],delimiters[1]))
                ranges.sort()
                for i in range(self.PACKET_SIZE):
                    skip=False
                    for delimiters in ranges:
                        if len(delimiters)>1:
                            if(i>=delimiters[0] and i<=delimiters[1]):
                                skip=True
                                break
                            elif delimiters[0]>i:
                                break
                            elif i>delimiters[1]:
                                ranges.remove(delimiters)
                        elif i==delimiters[0]:
                            skip=True
                            ranges.remove(delimiters)
                            break
                    if skip: continue
                    # Read packet
                    start_ind=i*self.PACKET_SIZE
                    with open(path_file, 'rb') as output:
                        output.seek(start_ind)
                        bytes_data=output.read(self.PACKET_SIZE)
                    payload = '{{"fn":{},"tt":{},"pn":{},"pt":{}}}'.format(
                        '"prueba.bmp"', num_packets, i, 
                        binascii.hexlify(bytes_data))
                    # Send packet
                    print(payload)
                    self.mqtt_connection.publish(
                        topic='sd_file',                    
                        payload=payload,
                        qos=mqtt.QoS.AT_LEAST_ONCE)



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
        #if text_data:
         #   text_data_json = json.loads(text_data)
            #message = text_data_json['message']
        if bytes_data:
            # Saving file temporarily
            path_file=settings.MEDIA_ROOT+"prueba.bmp"
            with open(path_file, 'wb') as output:
                output.write(bytes_data)
            #imagestring = bytearray(bytes_data)
            num_packets=int(1+(len(bytes_data)/self.PACKET_SIZE))
            for i in range(num_packets):
                print("Sending packet "+str(i)+" from "+str(num_packets))
                start_ind=i*self.PACKET_SIZE
                end_ind=start_ind+self.PACKET_SIZE
                payload = '{{"d":{}}}'.format(
                    '"prueba.bmp"')
                self.mqtt_connection.publish(
                    topic=self.ACCEPT_STREAM_TOPIC,                    
                    payload=payload,
                    qos=mqtt.QoS.AT_LEAST_ONCE)