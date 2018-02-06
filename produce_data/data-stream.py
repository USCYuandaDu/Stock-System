# read from any kafka
# write to any kafka
# perform average on stocks every 5 seconds

import argparse
from kafka import KafkaProducer
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

topic_name = None
kafka_broker = None
target_topic = None
kafka_producer = None

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('topic_name', help='the name of the topic')
	parser.add_argument('kafka_broker', help='the location of the kafka')
	parser.add_argument('target_topic', help='the new topic to write to')

	args = parser.parse_args()
	topic_name = args.topic_name
	kafka_broker = args.kafka_broker
	target_topic = args.target_topic

	sc = SparkContext('local[2]', 'stock-price-analysis')
	sc.setLogLevel('INFO')
	ssc = StreamingContext(sc, 5)

	directKafkaStream = KafkaUtils.createDirectStream(ssc, [topic_name], {'metadata.broker.list':kafka_broker})


	kafka_producer = KafkaProducer(
		bootstrap_servers=kafka_broker
	)
