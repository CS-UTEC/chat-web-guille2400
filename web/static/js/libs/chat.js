function sendMessage(name){
    alert("Holaaaaaaaaaaa" + name);
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
}

function get_users(){
    console.log("Voy a traer a todos los usuarios");
    $.getJSON("/users", function(data)
    {
    let i =0;
    $.each(data, function()
    {
    var div = '<div onclick="sendMessage(\'p_name\')"><span>username</span></div>';
    div = div.replace("username", data[i]['username']);
    div = div.replace("p_name", data[i]['username']);
    $('#contacts').append(div);
    i = i+1;

    })
    });
}