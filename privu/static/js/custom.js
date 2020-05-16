function delitem(filecode){
    $.ajax({
        url: '/deletefile' ,
        type: "POST",
        async: false,
        contentType: "application/json",
        data: JSON.stringify({"filecode": filecode}),
        success : function(data) {
            window.location.reload();
        }
    });
};

function logout() {
    $.ajax({
        url: '/logout' ,
        type: "GET",
        async: false,
        success : function(data) {
            window.location.reload();
        }
    });
};
