# read data from kafak
# send to redis pub

from kafka import KafkaConsumer

import logging
import argparse

logging.basicConfig()
logger = logging.getLogger('redis-publisher')
logger.setLevel(logging.DEBUG)

topic_name = None
kafka_broker = None

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('topic_name', help = 'kafka topic')
	parser.add_argument('kafka_broker', help = 'kafka kafka_broker')
	parser.add_argument('redis_host', help = 'the host_name of redis')
	parser.add_argument('redis_port', help = 'the port of redis')
	parser.add_argument('redis_channel', help = 'the channel of redis to publish')

	args = parser.parse_args()
	topic_name = args.topic_name
	kafka_broker = args.kafka_broker
	redis_host = args.redis_host
	redis_port = args.redis_port
	redis_channel = args.redis_channel

	# setup kafka consumer
	kafka_consumer = KafkaConsumer(
		topic_name,
		bootstrap_servers = kafka_broker
	)

	redis_client = redis.StrictRedis(host = redis_host, port = redis_port)

	for msg in kafka_consumer:
		logger.info('received data from kafka %s' % str(msg))
		redis_client.publish(redis_channel, msg.value)




