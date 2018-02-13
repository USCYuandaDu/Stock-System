# Stock-System

# Description

Built data pipline to store and analyze data in real time.

Used Spark to speed up the computation process.

Stored the data with Cassandra beacuse it has linear capacity scalability and is easy to operate.

# Docker

A tool to package and deploy applications inside containers

Client Server Architecture:

1\. Docker Client: A small client to communicate with Docker Daemon.

2\. Docker Daemon: A background daemon running on host servers.

3\. Docker Registry: A warehouse for containers images.

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

docker run -d -p 9092:9092 -e KAFKA\_ADVERTISED\_HOST\_NAME=localhost -e KAFKA\_ADVERTISED\_PORT=9092 --name kafka --link zookeeper:zookeeper confluent/kafka

Docker will download the image if it can not find locally.

# Zookeeper

An open source distributed system to coordinate node.

To make building and coordinate the distributed system easier.
