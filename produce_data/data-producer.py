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
#atexit can be used to register shutdown_hook
import atexit

from kafka import KafkaProducer
from yahoo_finance import Share

logging.basicConfig()
logger = logging.getLogger('data-producer')

#debug < info < warn < error < fatal
# we could ouly see the log if its level greater or equal than DEBUG
logger.setLevel(logging.DEBUG)

symbol = ''
topic_name = ''
kafka_broker = ''


def shutdown_hook(producer):
	logger.info('closing kafka producer')
	producer.flash(10)
	producer.close(10)
	logger.info('kafka producer closed')


def fetch_price_and_send(producer, stock):
	logger.debug('about to fetch price')
	stock.refresh()
	price = stock.get_price()
	trade_time = stock.get_trade_datetime()
	data = {
		'symbol': symbol,
		'last_trade_time': trade_time,
		'price': price
	}
	data = json.dump(data)
	logger.info('retrieved stock price % s', data)

	try:
		producer.send(topic=topic_name, value=data)
		logger.debug('sent data to kafka %s', data)
	except Exception as e:
		logger.warn('failed to send price to kakfa')

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

	stock = Share(symbol)

	schedule.every(1).second.do(fetch_price_and_send, producer, stock)

	#register the shutdown_hook to atexit
	atexit.register(shutdown_hook, producer)
	while True:
		schedule.run_pending()
		time.sleep(1)








