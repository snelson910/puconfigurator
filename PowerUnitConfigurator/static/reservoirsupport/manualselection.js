function search(){
    query = $("#query").val();
    $.ajax({
        url: "search",
        type: "POST",
        data: {
            csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            query: query
        },
        success: function(response)
            {
                console.log(response);
            },
        error: function()
        {
            console.log("Error")
        }
    });
}