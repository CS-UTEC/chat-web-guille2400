function sendMessage(name){
    alert("Holaaaaaaaaaaa" + " " + name);
}
function get_current(){
    console.log("Voy a traer el usuario logueado");
    $.getJSON("/current", function(data)
    {
    console.log(data['username'])
    var div = "<div><span>username</span></div>";
    div = div.replace("username", data['username']);
    $('#contacts').append(div);
    get_users();
    });
    get_users(data['id']);
}

function get_users(user_from_id){
    console.log("Voy a traer a todos los usuarios");
    $.getJSON("/users", function(data)
    {
    let i =1;
    $.each(data, function()
    {
    var div = '<div onclick="get_messages(\'user_to_id\', \'user_from_id\')"><span>username</span></div>';
    div = div.replace("username", data[i]['username']);
    div = div.replace("p_name", data[i]['username']);
    div = div.replace("user_from_id", user_from_id);
    div = div.replace("user_to_id", data[i]['id']);

    $('#contacts').append(div);
    i = i+1;
    
    })
    });

} 

function get_messages(user_from_id, user_to_id){
    $('#chat').empty();
    console.log(user_to, user_from)
    $.getJSON("/messages/" +user_from_id + "/" + user_to_id , function (data){
        let i =0;
        $.each(Data, function ()
        {
            let div = '<div>Content</div>';
            div = div.replace('Content', data[i]['content']);
            $('#boxMessage').append(div);
            i = i+1;
        })
    })
}