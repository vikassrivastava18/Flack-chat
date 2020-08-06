
document.addEventListener('DOMContentLoaded',start);
// Start the socket server
function start(){
socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');
// Send an event to server on socket connection
socket.on('connect', function(){
    const date = new Date();
    const timestamp = date.getTime();
    console.log(timestamp);
    socket.emit('joined', {time:timestamp});
});
// Append a joining message
socket.on('status',function(data){
    addPost(data);
});
// Sending a message in room
document.querySelector('#chatbutton').addEventListener('click',function(){
const text = document.querySelector('#chatMessage').value;
socket.emit('post',{msg:text});
document.querySelector('#chatMessage').value = '';  
});

// Append the message in html for this room
socket.on('showmessage',function(data){
    console.log('data came');
    addPost(data);
});

function addPost(message){
    const post = document.createElement('div');
    post.className='postnew';
    const mg = message.mg.text;
    const names = message.mg.name;
    //const timejoined = 'now';
    const timejoined = message.mg.timestamp;
    post.innerHTML='<span id ="messageChat">' + names + '</span>' + '<span class = "nameChat">' + mg + '</span>' + '<span>'+ timejoined +'</span>' +'<button class="hide">' + 'hide' + '</button>';
    document.querySelector('#newPost').prepend(post);
}
}