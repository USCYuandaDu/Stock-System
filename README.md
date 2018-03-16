# Stock-System

# Description

Built data pipline to store and analyze data in real time.


# Docker

A tool to package and deploy applications inside containers

### Client Server Architecture:

1\. Docker Client: A small client to communicate with Docker Daemon.

2\. Docker Daemon: A background daemon running on host servers.

3\. Docker Registry: A warehouse for containers images.

### Installation:

Download from APP store and start it.

# Data Ingestion Layer:

1.High throughput

2.Merely a pass through

3.Simple processing logic

4.Cannot serve as storage layer

# Kafka

An open source distributed messaging system.

Used it to make data transportation easier.

### Attributes:

1.fast - hundreds MB/s from thousands of client.

2.Scalable - easily scale up and down without downtime.

3.Durable - Messages are persisted on disk to prevent data loss.

### PULL vs PUSH:

1.Push - high throughput, complex server logic.

2.Pull - low throughput, simple server logic.

3.Producers use push model and consumers use pull model

### Topic and Partition:

phiscally, topic is made up partitions which could store more data and reach data quickly.

It used log file(partitions) to store the messages. The messages would store certain time.

One partition is a directory. And phiscally one partition is stored in many files which name is the offset.

It also has a sliding window to delete the old data.


### IO optimization:

1.append only writing so that read do not block write

2.One partition is a one long file.(sequential IO is fast than random access)

3.zero copy, do not copy data from kernel to application

### Consumer Group:

A group of consumers.

### Data replication:

1.Producer write through partition leader.

2.Partition leader write the messages into the local disks

3.Partition followers pull data from the Leader.

4.When Leader recieve enough ACK from the partition followers, it's written.


### Dependencies:

1.scala

2.sbt

3.python

4.pip

### Installation and run:


docker run -d -p 9092:9092 -e KAFKA_ADVERTISED_HOST_NAME=localhost -e KAFKA_ADVERTISED_PORT=9092 --name kafka --link zookeeper:zookeeper confluent/kafka



Docker will download the image if it can not find locally.

# Zookeeper

An open source distributed system to coordinate node.

To make building and coordinate the distributed system easier.

### Attributes:
1.Strong consistency, ordering, and durability guarantees.
2.The ability to implement typical synchronization primitives.
3.A simpler way of dealing with concurrency.

### Installation:
docker run -d -p 2181:2181 -p 2888:2888 -p 3888:3888 --name zookeeper confluent/zookeeper

### Master-Slave Model:

1.Master knows a list of tasks

2.Master in charge of distrbuting tasks

3.Slaves in charge of executing tasks

4.Slaves need to report status back to Master

problem: Master Election, Crash Detection, Group membership, Metadata management

### Ways to coordinate:

1.Message passing

2.Shared storage(Zookeeper)

### Split-brain Example:

1.In a system, we have one master, one backup master, and many workers.

2.Part of the workers are having trouble to reach master.

3.Connect with backup master instead.

### Data Tree:

1.Organized in hierarchical structure

2.Similar to file system

3.Kafka could connect all brokers through one borker by zookeeper, because all brokers info are stored in zookeeper.

### Znode:

1.Basic unit of Data Tree

2.Persisent Znode, Ephermal Znode and Sequential Znode

### Watcher:

1.Help client to know changes to znodes, zookeeper push a notification

### Leader Election within Zookeeper:

Server has following mode: Leader, Follower, Observer

### State Replication within Zookeeper:
Zab protocal

Leader:
1.Receives write requests

2.convert requests into transaction

3.Leader send proposal message to all follower

4.Once receiving ack from a quorum, leader sends commit message

Follower:
1.Received Proposal message from leader

2.Check if the leader is the correct leader

3.Check if the transaction is in correct order

4.Send ack back to leader

5.Received COMMIT message from leader

6.apply change to the Data Tree
### Client-Server Interaction:

1.Connection: TCP connection, Client only connects to server with newer/equal state, configurable session timeout

# Data storage layer

1.High availablity

2.Fault tolerance

3.Handles high data volume

4.Able to handle various type of data

### OLTP vs OLAP

transactional data vs analytical data

### Common storage problems:

users are getting slow read ? 

1. Read/Write separation: a.write to primary master b.read from all the nodes c.replication to copy data so that write won't block read

2. Add Caching: a.hit cache before hitting DB b. move reads into in memory cache

3. Shard/Partition data based on some rules


# Cassandra
An open source distributed storage system that provides high availability.

### Gossip Protocal(spead messages like who is down):

1.Push: a.upon reception, every node forward messages to multiple other nodes b. low latency, high redundancy(cassandra used)

2.Pull: a.every node periodically contact other nodes fo missing information b. high latency, low redundancy
 
3.Gossip protocal can pass outdated information

4.Or cassandra uses seed nodes to stabilize the cluster, seed nodes are contacted by other nodes when they start up.

### Data Model:

1.Every name/value pair is a column

2. Add a row key to be able to reference an "entity"

3.Group of rows can be think as a table (column family)

4.Multiple tables becomes keyspace

### Commit Log

1.crash-recovery mechanism

2.all write operation is immediately written to commit log


### MemTable

### SSTable

1.content of memtable gets written to SSTable after memtable if full

2.Immutable cannot be changed

3.Changes are appended

4.Sequential write to disk


### Compaction:

1.Merge of SSTables

2.New merged data is sorted as well (sorted by row key and col key)

3.Reduce number of seeks

### Consistent Hashing
1.Each node is assigned one or more ranges of data identified by Token
2.A node owns the range of values <= to the token and > the token of previous node
3.Nodes moving will only affect small ranges of data

### start Cassandra:
docker run -d -p 7199:7199 -p 9042:9042 -p 9160:9160 -p 7001:7001 --name cassandra cassandra:3.7


