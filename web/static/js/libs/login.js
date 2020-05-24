function login(){
        console.log("LOGIN USER"); //permite esribir en la consola del navegador
        var username = $('#username').val(); //getting username by id
        var password = $('#password').val(); //getting username by id
        console.log("DATA>",username, password); //print de la data obtenido
        var credentials = {'username' : username, 'password':password}; //Creamos objeto para almacenar el username y password recojido
        $.post({
            url: '/authenticate',
            type: 'post',
            dataType: 'json',
            contentType: 'application/json',
            success: function(data)
            {
                console.log("Authenticate!");
                alert("Authenticate!!!");
            },
            data: JSON.stringify(credentials)

        });

}