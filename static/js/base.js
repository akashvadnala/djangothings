function modaldel()
{
    document.getElementById('id01').style.display='none';
    document.getElementById('id02').style.display='none';
    document.getElementById('modal-del').style.display='none';
}

  var swiper = new Swiper('.swiper-container', {
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    },
  });


function checkuser(){
    let un = document.getElementById("username").value;
    let orgi = document.getElementById("orgi");
    dub = document.getElementById("dub");
    $.ajax({
        url:"{% url 'check_user' %}",
        type:"get",
        data:{usern:un},
        success:function(data){
            $("#result").html(data);
            $("#orgi").css("display","block");
            $("#dub").css("display","none");
        }
    })
    
}


$( document ).ready(function() {
    $('.like-form').submit(function(e){
        e.preventDefault()
        const book_id = $(this).attr('id')
        const likeText = $(`.like-btn${book_id}`).text()
        const trim = $.trim(likeText)
        const url = $(this).attr('action')
        let res;
        const likes = $(`.like-count${book_id}`).text()
        const trimCount = parseInt(likes)
        $.ajax({
            type:'POST',
            url:url,
            data: {
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                'book_id':book_id,
            },
            success:function(response){
                    if(response.liked===true){
                        $(`.liking${book_id}`).css('color','red')
                        $(`.liking${book_id}`).css('transition','.5s')
                        $(`.liking${book_id}`).addClass('fa-heart')
                        $(`.liking${book_id}`).removeClass('fa-heart-o')
                        res = trimCount-1
                    }
                    else{
                        $(`.liking${book_id}`).css('color','grey')
                        $(`.liking${book_id}`).addClass('fa-heart-o')
                        $(`.liking${book_id}`).removeClass('fa-heart')
                        res = trimCount+1
                    }
                    $(`.like-count${book_id}`).text(response.likes_count)
               },
               error:function(response){
                console.log('error', response)
               }
        })
    })
});




