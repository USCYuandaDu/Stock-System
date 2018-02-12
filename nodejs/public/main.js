$(function() {
	var socket = io();
	console.log('created socketio client');

	socket.on('data', function(data) {
		console.log(data);
	});
});