let currentRecipient = '';
let chatInput = $('#chat-input');
let chatButton = $('#btn-send');
let userList = $('#user-list');
let messageList = $('#messages');
let con = $('#side-container-box');
let activeUser = $('.active');


function putnotification(rec,sender,reciver){
    $.ajax({
        type:'GET',
        url: 'chat/putnotif/',
        data:{
            'rec':rec,
            'sender':sender,
            'reciver':reciver,
        },
        dataType:'json',
        success: function(data){
            updateUserList();
        }
    });
}

function removenotification(rec){
    $.ajax({
        type:'GET',
        url: 'chat/removenotif/',
        data:{
            'rec':rec,
        },
        dataType:'json',
        success: function(data){
            updateUserList();
        }
    });
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
    $.ajax({
        type:'GET',
        url: 'chat/getusers/',
        success: function(data){
            userList.children('.user').remove();
            $('#user-list').empty();
            for (let i = 0; i < data.length; i++) {
                const userItem = `
                    <div type="button" onclick="get_user('${data[i]['username']}')" class="user-one user ${data[i]['username']}" id="user-one ${data[i]['username']}">
                        <div class="user-s">    
                            <span>${data[i]['username']}</span>
                            <span class="msg_not" style="display:${data[i]['display']}; color:cornflowerblue; border:solid 1px cornflowerblue;">${data[i]['msg_count']}</span>
                        </div>
                        <div class="last_msg" style="display:${data[i]['atuser']};">
                            ${data[i]['last_msg']}
                        </div>
                    </div>
                `;
                $(userItem).appendTo('#user-list');
        }
        let user = $('#msg-head').text();
        userList.children(".active").removeClass("active");
        $('.'+user).addClass("active");
    }
    
});
    /*
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

        $('#user-one').click(function (event) {
            userList.children('.active').removeClass('active');
            let selected = event.target;
            $(selected).addClass('active');
            $('#msg-head').text(selected.text);
            setCurrentRecipient(selected.text);
        });*/
   
}


function get_user(user){
    userList.children(".active").removeClass("active");
    $('.'+user).addClass("active");
    $(".msg-list").css('display','block');
    $('#msg-head').text(user);
    removenotification(user);
    updateUserList();
    setCurrentRecipient(user);
}

function drawMessage(message) {
    let position = 'left';
    const date = new Date(message.timestamp);
    if (message.user === currentUser) position = 'right';
    if (message.body === ''){
        if(message.user === currentUser){
            const messageItem = `
            <li class="message mid">
                <div class="avatar">
                    <span>${message.msg2}</span>
                    <!--span>${message.user}</span>
                    <span class="small">${date}</span-->
                </div>
            </li>`;
            $(messageItem).appendTo('#messages');
        }
        else{
            const messageItem = `
            <li class="message mid">
                <div class="avatar">
                    <span>${message.msg1}</span>
                    <!--span>${message.user}</span>
                    <span class="small">${date}</span-->
                </div>
            </li>`;
            $(messageItem).appendTo('#messages');
        }
    }
    else{
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
}

function getConversation(recipient) {
    $.getJSON(`api/v1/message/?target=${recipient}`, function (data) {
        messageList.children('.message').remove();
        for (let i = data['results']['length'] - 1; i >= 0; i--) {
            drawMessage(data['results'][i]);
        }
        messageList.animate({scrollTop: messageList.prop('scrollHeight')});
        con.animate({scrollTop: con.prop('scrollHeight')});
    });

}
/*
function getConversation(rec){
    $.ajax({
        type:'GET',
        url: 'chat/getmessages/',
        data:{
            'rec':rec,
        },
        dataType:'json',
        success: function(data){
            messageList.children('.message').remove();
            for (let i = data.length - 1; i >= 0; i--) {
                drawMessage(data[i]);
            }
            messageList.animate({scrollTop: messageList.prop('scrollHeight')});
            con.animate({scrollTop: con.prop('scrollHeight')});
        }
    });
}*/

function sendMessage(recipient, body) {
    $.post('api/v1/message/', {
        recipient: recipient,
        body: body,
    }).fail(function () {
        alert('Hello Error! Check console!');
    });
    updateUserList();
}

function setCurrentRecipient(username) {
    currentRecipient = username;
    getConversation(currentRecipient);
    enableInput();
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
        putnotification(currentRecipient,data.user,data.recipient);
        updateUserList();
    });
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

function inc_num(rec,user){
    $.ajax({
        type:'GET',
        url: 'chat/incnum/',
        data:{
            'rec':rec,
            'user':user,
        },
        dataType:'json',
        success: function(){

        }
    });
}

$('#userChat').keypress(function (e) {
    let rec = $('#userChat').val();
    if (e.keyCode == 13){
        $.ajax({
            type:'GET',
            url: 'chat/userinp/',
            data:{
                'rec':rec,
            },
            dataType:'json',
            success: function(data){
                if(data.all){

                }
                else if(data.created)
                {
                    const userItem = `
                        <div type="button" onclick="get_user('${data['username']}')" class="user-one user ${data['username']}" id="user-one ${data['username']}">
                            ${data['username']}
                        </div>
                    `;
                    $(userItem).appendTo('#user-list');
                }
                else if(data.got){
                    userList.children('.user').remove();
                    const userItem = `
                        <div type="button" onclick="get_user('${data['username']}')" class="user-one user ${data['username']}" id="user-one ${data['username']}">
                            ${data['username']}
                        </div>
                    `;
                    $(userItem).appendTo('#user-list');
                }
            }
        });
    }            
});


$(document).ready(function () {
    updateUserList();
    disableInput();

//    let socket = new WebSocket(`ws://127.0.0.1:8000/?session_key=${sessionKey}`);
    ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var socket = new WebSocket(
        ws_scheme + '://' + window.location.host +
        '/notifications/ws?session_key=${sessionKey}')

    chatInput.keypress(function (e) {
        if (e.keyCode == 13)
            chatButton.click();            
    });

    chatButton.click(function () {
        if (chatInput.val().length > 0) {
            inc_num(currentRecipient,currentUser)
            sendMessage(currentRecipient, chatInput.val());
            chatInput.val('');
            updateUserList();
        }
    });

    socket.onmessage = function (e) {
        getMessageById(e.data);
        updateUserList();
    };
});



