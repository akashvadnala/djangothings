let currentRecipient = '';
let chatInput = $('#chat-input');
let chatButton = $('#btn-send');
let userList = $('#user-list');
let messageList = $('#messages');
let con = $('#side-container-box');

function get_user(user){
    userList.children('.active').removeClass('active');
    $('#'+user).addClass('active');
    $('.msg-list').css('display','block');
    $('#msg-head').text(user);
    setCurrentRecipient(user);
}
/*
$(document).ready(function(){
    //setInterval(function(){
      $.ajax({
          type: 'GET',
          url : "{% url 'getusers %}",
          success: function(response){
              console.log(response);
             $("#user-list").empty();
               for (var key in response.messages)
               {
                   var temp="<div class='container darker'><b>"+response.messages[key].user+"</b><p>"+response.messages[key].value+"</p><span class='time-left'>"+response.messages[key].date+"</span></div>";
                   $("#user-list").append(temp);
                    
               }
              
          },
          error: function(response){
              alert('An error occured')
          }
      });
    //},1000);
  })*/


function updateUserList() {
    $.getJSON('api/v1/user/', function (data) {
        userList.children('.user').remove();
        
        for (let i = 0; i < data.length; i++) {
            const userItem = `
                <div type="button" onclick="get_user('${data[i]['username']}')" class="user-one user" id="user-one ${data[i]['username']}">
                    ${data[i]['username']}
                </div>
            `;
            $(userItem).appendTo('#user-list');
        }
/*
        $('#user-one').click(function (event) {
            userList.children('.active').removeClass('active');
            let selected = event.target;
            $(selected).addClass('active');
            $('#msg-head').text(selected.text);
            setCurrentRecipient(selected.text);
        });*/
    });
}

function drawMessage(message) {
    let position = 'left';
    const date = new Date(message.timestamp);
    if (message.user === currentUser) position = 'right';
    const messageItem = `
            <li class="message ${position}">
                <div class="avatar">
                    <span>${message.body}</span>
                    <!--span>${message.user}</span>
                    <span class="small">${date}</span-->
                </div>
            </li>`;
    $(messageItem).appendTo('#messages');
}

function getConversation(recipient) {
    $.getJSON(`api/v1/message/?target=${recipient}`, function (data) {
        messageList.children('.message').remove();
        for (let i = data['results'].length - 1; i >= 0; i--) {
            drawMessage(data['results'][i]);
        }
        messageList.animate({scrollTop: messageList.prop('scrollHeight')});
        con.animate({scrollTop: con.prop('scrollHeight')});
    });

}

function getMessageById(message) {
    id = JSON.parse(message).message
    $.getJSON(`api/v1/message/${id}/`, function (data) {
        if (data.user === currentRecipient ||
            (data.recipient === currentRecipient && data.user == currentUser)) {
            drawMessage(data);
        }
        messageList.animate({scrollTop: messageList.prop('scrollHeight')});
        con.animate({scrollTop: con.prop('scrollHeight')});
    });
}

function sendMessage(recipient, body) {
    $.post('api/v1/message/', {
        recipient: recipient,
        body: body
    }).fail(function () {
        alert('Hello Error! Check console!');
    });
}

function setCurrentRecipient(username) {
    currentRecipient = username;
    getConversation(currentRecipient);
    enableInput();
}


function enableInput() {
    chatInput.prop('disabled', false);
    chatButton.prop('disabled', false);
    chatInput.focus();
}

function disableInput() {
    chatInput.prop('disabled', true);
    chatButton.prop('disabled', true);
    $('.msg-list').css('display','block');
}

$(document).ready(function () {
    updateUserList();
    disableInput();

//    let socket = new WebSocket(`ws://127.0.0.1:8000/?session_key=${sessionKey}`);
    var socket = new WebSocket(
        'ws://' + window.location.host +
        '/notifications/ws?session_key=${sessionKey}')

    chatInput.keypress(function (e) {
        if (e.keyCode == 13)
            chatButton.click();
    });

    chatButton.click(function () {
        if (chatInput.val().length > 0) {
            sendMessage(currentRecipient, chatInput.val());
            chatInput.val('');
        }
    });

    socket.onmessage = function (e) {
        getMessageById(e.data);
    };
});



