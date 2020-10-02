var data;
var data2;
var pumpnum;
var pumpcurrent = 0;
var selected;
var max = 0;
var flow;
var reservoir;
var motor;
var accountnumber;
var pumparray = []; 
var througharray = [];
var motorarray = [];
var reservoirarray = [];
var frame = "";
var frontpump = "";

function cookiecheck(){
    var ac = document.cookie;
    ca = ac.split(';');
    for(x in ca){
        key = ca[x].split('=')[0];
        value = ca[x].split('=')[1];
        if(key == " an"){
            accountnumber = value;
        }
        if(key == ' pumps'){
            pumparray = JSON.parse(value);
        }
        if(key == ' throughdrives'){
            througharray = JSON.parse(value);
        }
        if(key ==' motor'){
            motorarray = [value];
        }
        if(key ==' reservoir'){
            reservoirarray = [value];
        }
        if(key == ' frame'){
            frame = value;
        }
        if(key == ' frontpump'){
            frontpump = value;
        }
    }

    throughtables();
}
function throughtables(){
    if(througharray.length > 0){
        $.ajax({
            url: "details",
            type: "POST",
            data: {
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
                arr: JSON.stringify(througharray)
            },
            success: function(response)
                {
                    parts = response.reverse();
                    for(x in parts){
                        $("#tr_pumps").after("<tr><td>" + parts[x][0] + "</td><td>" + parts[x][1] + "</td><td>" + parts[x][2] +"</td><td>$" + parts[x][3] +"</td><td>" + 
                        parts[x][4] + "</td><td>" + parts[x][5] +"</td></tr>");   
                    }
                    pumptables();
                },
            error: function()
            {
                console.log("Error")
            }
        });
    }
    else{
        pumptables();
    }
}
function pumptables(){
    if(pumparray.length > 0){
        $.ajax({
            url: "details",
            type: "POST",
            data: {
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
                arr: JSON.stringify(pumparray)
            },
            success: function(response)
                {
                    pumps = response.reverse();
                    for(x in pumps){
                        $("#tr_pumps").after("<tr><td>" + pumps[x][0] + "</td><td>" + pumps[x][1] + "</td><td>" + pumps[x][2] +"</td><td>$" + pumps[x][3] +"</td><td>" + 
                        pumps[x][4] + "</td><td>" + pumps[x][5] +"</td></tr>");
                    }
                    motortables();
                },
            error: function()
            {
                console.log("Error")
            }
        });        
    }
    else{
        motortables();
    }
}
function motortables(){
    if(motorarray.length > 0){
        $.ajax({
            url: "details",
            type: "POST",
            data: {
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
                arr: JSON.stringify(motorarray)
            },
            success: function(response)
                {
                    for(x in response){
                        $("#tr_motors").after("<tr><td>" + response[x][0] + "</td><td>" + response[x][1] + "</td><td>" + response[x][2] +"</td><td>$" + response[x][3] +"</td><td>" + 
                        response[x][4] + "</td><td>" + response[x][5] +"</td></tr>");
                    }
                    reservoirtables();
                },
            error: function()
            {
                console.log("Error")
            }
        });
    }
    else{
        reservoirtables();
    }
}
function reservoirtables(){
    if(reservoirarray.length > 0){
        $.ajax({
            url: "details",
            type: "POST",
            data: {
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
                arr: JSON.stringify(reservoirarray)
            },
            success: function(response)
                {
                    for(x in response){
                        $("#tr_reservoirs").after("<tr><td>" + response[x][0] + "</td><td>" + response[x][1] + "</td><td>" + response[x][2] +"</td><td>$" + response[x][3] +"</td><td>" + 
                        response[x][4] + "</td><td>" + response[x][5] +"</td></tr>");
                    }
                },
            error: function()
            {
                console.log("Error")
            }
        });
    }
    couplingtables();
}

function couplingtables(){
    if(frame != "" && frontpump != ""){
        $("#tr_couplings").removeAttr("hidden", "hidden");
        $.ajax({
            url: "manual/coupling",
            type: "POST",
            data: {
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
                pump: frontpump,
                motor: motorarray[0]
            },
            success: function(response)
                {
                    for(x in response){
                        $("#tr_couplings").after("<tr><td>" + response[x][0] + "</td><td>" + response[x][1] + "</td><td>" + response[x][2] +"</td><td>$" + response[x][3] +"</td><td>" + 
                        response[x][4] + "</td><td>" + response[x][5] +"</td></tr>");
                    }
                },
            error: function()
            {
                console.log("Error")
            }
        });
    }
}