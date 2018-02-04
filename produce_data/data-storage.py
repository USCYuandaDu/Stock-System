#read from any kafka
#write to any cassandra

import argparse
import logging
import json
import atexit
import requests
from cassandra.cluster import Cluster
from kafka import KafkaConsumer
from py_zipkin.zipkin import zipkin_span
from py_zipkin.thread_local import get_zipkin_attrs
from py_zipkin.zipkin import ZipkinAttrs
from py_zipkin.util import generate_random_64bit_string

topic_name = ''
kafka_broker = ''
cassandra_broker = ''
keyspace = ''
table = ''

logging.basicConfig()
logger = logging.getLogger('data-storage')
logger.setLevel(logging.DEBUG)

def http_transport_handler(span):
   requests.post('http://localhost:9411/api/v1/spans', data = span, headers={'Content-Type':'application/x-thrift'})

def construct_zipkin_attrs(data):
    parsed = json.loads(data)
    return ZipkinAttrs(
        trace_id = parsed.get('trace_id'),
        parent_span_id = parsed.get('parent_span_id'),
        is_sampled = parsed.get('is_sampled'),
        flags = '0',
        span_id = generate_random_64bit_string()
    )

def shutdown_hook(consumer, session):
    logger.info('closing resource')
    consumer.close()
    session.shutdown()
    logger.info('released resource')

def save_data(stock_data, session):
    zipkin_attrs = construct_zipkin_attrs(stock_data)
    with zipkin_span(service_name='data_storage', span_name='save_data', transport_handler = http_transport_handler, zipkin_attrs=zipkin_attrs):
        try:
            logger.debug('start to save the data %s', stock_data)
            parsed = json.loads(stock_data)
            symbol = str(parsed.get('symbol'))
            price = float(parsed.get('price'))
            timestamp = parsed.get('last_trade_time')
            statement = "INSERT INTO %s (symbol, trade_time, price) VALUES ('%s', '%s', %f)" % (table, symbol, timestamp, price)
            session.execute(statement)

        except Exception as e:
        	print e


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('topic_name', help='the kafka topic to subscribe from')
    parser.add_argument('kafka_broker', help='the location of the kafka broker')
    parser.add_argument('cassandra_broker', help='the cassandra broker location')
    parser.add_argument('keyspace', help='the keyspace to use in cassandra')
    parser.add_argument('table', help='the data table to use')
    # parser.add_argument('contact_points', help='the contact points for cassandra')

    # - parse arguments
    args = parser.parse_args()
    topic_name = args.topic_name
    kafka_broker = args.kafka_broker
    keyspace = args.keyspace
    table = args.table
    cassandra_broker = args.cassandra_broker

    consumer = KafkaConsumer(
    	topic_name,
    	bootstrap_servers = kafka_broker
    )

    cassandra_cluster = Cluster(
    	contact_points = cassandra_broker.split(",")
    )

    session = cassandra_cluster.connect()

    session.execute("CREATE KEYSPACE IF NOT EXISTS %s WITH replication = {'class':'SimpleStrategy', 'replication_factor':'1'}" % keyspace)
    session.set_keyspace(keyspace)
    session.execute("CREATE TABLE IF NOT EXISTS %s (symbol text, trade_time timestamp, price float, PRIMARY KEY (symbol, trade_time))" % table)

    atexit.register(shutdown_hook, consumer, session)
    for msg in consumer:
    	# logger.debug(msg)
    	save_data(msg.value, session)















