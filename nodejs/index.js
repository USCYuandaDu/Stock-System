// -get command line argument

var argv = require('minimist')(process.argv.slice(2))

var redis_host = argv['redis_host'];
var redis_port = argv['redis_port'];
var redis_channel = argv['redis_channel'];

var express = require('express');
var app = express();
var server = require('http').createServer(app);

// setup redis client

var redis = require('redis');
console.log('create redis client');

var redisClient = redis.createClient(redis_port, redis_host);
console.log('subcribe to redis topic %s', redis_channel);

redisClient.subscribe(redis_channel);

// register redis callback function

redisClient.on('message', function(channel, message) {
	if(channel == redis_channel) {
		console.log('message received %s', message);
	}
});

app.use(express.static(__dirname = './public'));

server.listen(3000, function() {
	console.log('server started at port 3000')
});