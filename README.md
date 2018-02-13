# Stock-System

# Description

Built data pipline to store and analyze data in real time.


Used Spark to speed up the computation process.
Stored the data with Cassandra beacuse it has linear capacity scalability and is easy to operate.

# Docker
A tool to package and deploy applications inside containers
Client Server Architecture:
1. Docker Client: A small client to communicate with Docker Daemon.
2. Docker Daemon: A background daemon running on host servers.
3. Docker Registry: A warehouse for containers images.
Installation:
Download from APP store and start it.

# Kafka
An open source distributed messaging system.
Used it to make data transportation easier.
Attributes:
1.fast - hundreds MB/s from thousands of client.
2.Scalable - easily scale up and down without downtime.
3.Durable - Messages are persisted on disk to prevent data loss.
Dependencies:
1.scala
2.sbt
3.python
4.pip
Installation and run:
docker run -d -p 9092:9092 -e KAFKA_ADVERTISED_HOST_NAME=localhost -e KAFKA_ADVERTISED_PORT=9092 --name kafka --link zookeeper:zookeeper confluent/kafka

Docker will download the image if it can not find locally.

# Zookeeper
An open source distributed system to coordinate node.
To make building and coordinate the distributed system easier.
Attributes:
1. Coordinate nodes with using shared storage.
Installation and run:
docker run -d -p 2181:2181 -p 2888:2888 -p 3888:3888 -- name zookeeper confluent/zookeeper

# Cassandra
An open source distributed storage system that provides high availability.
Inspired by Amazon DynamoDB and Google BigTable
Installation and run:
docker run -d -p 7199:7199 -p 9042:9042 -p 9160:9160 -p 7001:7001 --name cassandra cassandra:3.7









