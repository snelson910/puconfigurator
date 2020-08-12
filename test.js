$(document).ready(function(){
    $("#testbutton").click(function(){
        var i = 5;
        for(x=0; x<i; x++){
            $("#testform").append(
                '<label for="' + x + '"> ' + x + ' </label> <input type="checkbox" id="' + x + '" name="' + x + '" value="' + x + '"><br>')
        }
        
    });
});
