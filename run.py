#! /usr/bin/env python3
from bottle import route, run, template
from pprint import pprint
from time import sleep
import json
import paho.mqtt.client as mqtt
import config

TOPICS = {}

def on_connect(client, userdata, flags, rc):
    client.subscribe(config.MQTT_TOPIC)

def dict_merge(x,y):
    """
    Stolen from: http://stackoverflow.com/questions/9730648/merge-a-nested-dictionary-default-values
    """
    # store a copy of x, but overwrite with y's values where applicable         
    merged = dict(x,**y)

    xkeys = x.keys()

    # if the value of merged[key] was overwritten with y[key]'s value           
    # then we need to put back any missing x[key] values                        
    for key in xkeys:
        # if this key is a dictionary, recurse                                  
        if isinstance(x[key], dict) and y.get(key, None):
            merged[key] = dict_merge(x[key],y[key])

    return merged

def merge_new_topic(new_topic):
    """
    Insert newly received topic into global dict of known topics
    """
    global TOPICS

    TOPICS = dict_merge(new_topic, TOPICS)

def generate_dict(topic, payload):
    """
    Create dictionary from the received topic
    """

    # Only save int or str values
    payload = payload.decode("utf-8")
    if isinstance(payload, str) or isinstance(payload, int):
        topic_dict = payload
    else:
        print(type(foo))
        topic_dict = "Data"

    # Split topic and build the dict from inside out
    splitted_topic = topic.split("/")
    splitted_topic.reverse()
    for part in splitted_topic:
        topic_dict = {part: topic_dict}

    return topic_dict


def on_message(client, userdata, msg):
    print("New Message: {}".format(msg.topic))
    # Generate dict from new_topic
    new_topic_dict = generate_dict(msg.topic, msg.payload)

    # Merge into known dicts
    merge_new_topic(new_topic_dict)


def convert(data):
    if isinstance(data,dict):
        children = []
        for key in data:
            children.append({"name":key,
                             "children": convert(data[key])})
        return children
    elif isinstance(data, str):
        return [{"name": data}]
    else:
        print("Type error: {}".format(data))


@route('/')
def index():
    return template('index')

@route('/get_topics')
def get_topics():
    tree = {"name": "root",
            "children": convert(TOPICS)}
    return json.dumps([tree])

# Start MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(config.BROKER_URL, config.BROKER_PORT, 60)
client.loop_start()

# Start Bottle server
run(host='localhost', port=8080)

