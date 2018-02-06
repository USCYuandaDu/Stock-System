# read from any kafka
# write to any kafka
# perform average on stocks every 5 seconds

import argparse
import json
import time
import atexit
import logging
from kafka import KafkaProducer
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

topic_name = None
kafka_broker = None
target_topic = None
kafka_producer = None

logging.basicConfig()
logger = logging.getLogger('data-stream')
logger.setLevel(logging.INFO)


def shutdown_hook(producer):
	producer.flush(10)
	producer.close(10)
	logger.info('closed')

def process_stream(stream):
	#perform avg based on different stock symbol
	# APPL

	def send_to_kafka(rdd):
		results = rdd.collect()
		for r in results:
			data = json.dumps(
				{
					'symbol': r[0],
					'average': r[1],
					'timestamp': time.time()
				}
			)
			logger.info(data)
			kafka_producer.send(target_topic, value=data)

	def preprocess(data):
		record = json.loads(data[1].decode('utf-8'))
		return record.get('symbol'), (float(record.get('price')), 1)

	stream.map(preprocess).reduceByKey(lambda a, b: (a[0] + b[0], a[1] + b[1])).map(lambda (k, v): (k, v[0]/v[1])).foreachRDD(send_to_kafka)


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
	sc.setLogLevel('WARN')
	ssc = StreamingContext(sc, 5)

	directKafkaStream = KafkaUtils.createDirectStream(ssc, [topic_name], {'metadata.broker.list':kafka_broker})
	process_stream(directKafkaStream)

	kafka_producer = KafkaProducer(
		bootstrap_servers=kafka_broker
	)
	atexit.register(shutdown_hook, kafka_producer)
	ssc.start()
	ssc.awaitTermination()


