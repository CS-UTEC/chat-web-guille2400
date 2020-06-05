function sendMessage(name){
    alert("Holaaaaaaaaaaa" + " " + name);
}
function get_current()
{
    console.log("Voy a traer el usuario logueado");
    $.getJSON("/current", function(data)
    {
    console.log(data['username']);
    var div = "<div><span>username</span></div>";
    div = div.replace("username", data['username']);
    $('#contacts').append(div);
    get_users(data['id']);
    });
}

function get_users(user_from_id){
    console.log("Voy a traer a todos los usuarios");
    $.getJSON("/users", function(data)
    {
    let i =1;
    $.each(data, function()
    {
    var div = '<div onclick="get_messages(user_to_id,user_from_id)"><span>username</span></div>';
    div = div.replace("username", data[i]['username']);
    div = div.replace("user_from_id", user_from_id);
    div = div.replace("user_to_id", data[i]['id']);

    $('#contacts').append(div);
    i = i+1;
    
    })
    });
} 

function get_messages(user_to_id, user_from_id)
{
    $('#inputBox').empty();
    $('#boxMessage').empty();
    console.log(user_to_id, user_from_id)
    $.getJSON("/messages/" +user_from_id + "/" + user_to_id , function (data){
        console.log(data)
        let i =0;
        $.each(data, function ()
        {
            let div = '<div>user_from_id</div><div>Content</div>';
            div = div.replace('user_from_id', data[i]['user_from_id'])
            div = div.replace('Content', data[i]['content']);
            $('#boxMessage').append(div);
            i = i+1;
        })
    })
    let inputBox = `<input type="text" size="100" id="txtMessage"><button type="button" class="btn btn-primary" onclick="send_messages(user_from_id,user_to_id)">Send</button>`
    inputBox = inputBox.replace('user_from_id',user_from_id)
    inputBox = inputBox.replace('user_to_id',user_to_id)
    $('#inputBox').append(inputBox);
}
function send_messages(user_from_id,user_to_id)
{
    var content = $('#txtMessage').val();
    var message = JSON.stringify({
        'content':content,
        'user_from_id':user_from_id,
        'user_to_id':user_to_id
    });
    $.post({
        url : '/messages',
        type : 'POST',
        dataType : 'json',
        contentType : 'application/json',
        data : message
    });
    get_messages(user_to_id, user_from_id)
}
