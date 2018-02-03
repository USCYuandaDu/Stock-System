# write data to any kafka cluster
# write data to any kafka topic
# schduled fetch price from yahoo finance
# configurable stock symbol



# parse command line argument
import argparse
import schedule
import logging
import time
import json
import datetime
import random
#atexit can be used to register shutdown_hook
import atexit

from kafka import KafkaProducer
from kafka.errors import KafkaError, KafkaTimeoutError
from yahoo_finance import Share

logging.basicConfig()
logger = logging.getLogger('data-producer')

#debug < info < warn < error < fatal
# we could ouly see the log if its level greater or equal than DEBUG
logger.setLevel(logging.DEBUG)

symbol = ''
topic_name = ''
kafka_broker = ''


# used KafkaConsumer to test the data
# >>> from kafka import KafkaConsumer
# >>> consumer = KafkaConsumer('stock-analyzer', bootstrap_servers='localhost:9092')
# >>> for msg in consumer:
# ...     print msg

def shutdown_hook(producer):
	logger.info('closing kafka producer')
	producer.flush(10)
	producer.close(10)
	logger.info('kafka producer closed')

def fetch_price_and_send(producer):
    logger.debug('Start to fetch stock price for %s', symbol)
    try:
        # price = json.dumps(getQuotes(symbol))
        price = random.randint(30, 120)
        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%dT%H:%MZ')
        payload = ('[{"StockSymbol":"AAPL","LastTradePrice":%d,"LastTradeDateTime":"%s"}]' % (price, timestamp)).encode('utf-8')

        logger.debug('Retrieved stock info %s', price)
        producer.send(topic=topic_name, value=str(price), timestamp_ms=time.time())
        logger.debug('Sent stock price for %s to Kafka', symbol)
    except KafkaTimeoutError as timeout_error:
        logger.warn('Failed to send stock price for %s to kafka, caused by: %s', (symbol, timeout_error.message))
    except Exception:
        logger.warn('Failed to fetch stock price for %s', symbol)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('symbol', help='the symbol of the stock')
	parser.add_argument('topic_name', help='the name of the topic')
	parser.add_argument('kafka_broker', help='the location of the kafka')

	args = parser.parse_args()
	symbol = args.symbol
	topic_name = args.topic_name
	kafka_broker = args.kafka_broker

	producer = KafkaProducer(
		# if we have kafka cluster with 1000 nodes, we do not need to pass these 1000 IPs to kafka_broker.
		bootstrap_servers=kafka_broker
	)

	#stock = Share(symbol)

	schedule.every(1).second.do(fetch_price_and_send, producer)

	#register the shutdown_hook to atexit
	atexit.register(shutdown_hook, producer)
	while True:
		schedule.run_pending()
		time.sleep(1)








