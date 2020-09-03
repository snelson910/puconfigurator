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
            console.log(value);
        }
        if(key == ' throughdrives'){
            console.log(value);
        }
    }
}

function chartconfig(){

}

$(document).ready(function(){
    $("#pumpnumsubmit").click(function(){
        $("#pumpnumsubmit").attr("disabled", "disabled");
        $("#pumpnums").attr("disabled", "disabled");
        $("#pumpnummodify").removeAttr("disabled","disabled");
        pumpnum = Number($("#pumpnums").val());
        max = pumpnum + 1;
        pumpcurrent ++;
        selected = "";
        if(pumpcurrent <= pumpnum){
            pumps();
        }
        else{
            //Pass
        }
    })
});
$(document).ready(function(){
    $("#pumpnummodify").click(function(){
        if(confirm("Are you sure? This will remove all later selections.")){
            for(i=0; i<max; i++){
                $("#pump" + i + "submit").remove();
                $(".pumpnumber" + i).remove();
                $("#pumpnumber" + i).remove();
            }
            pumpcurrent = 0;
            $("#pumpnums").removeAttr("disabled", "disabled");
            $("#pumpnumsubmit").removeAttr("disabled", "disabled");
            $("#pumpnummodify").attr("disabled","disabled");
            $("#reservoirs").empty();
            $("#reservoirconfiguration").attr("hidden", "hidden");
            $(".pumpmod").attr("hidden", "hidden");
        }else{
            //Pass.
        }
    });
});
function pumps(){
    $.ajax({
        url: "manual/pumps",
        type: "POST",
        data: {
            csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            pumpnum: pumpnum,
            pumpcurrent: pumpcurrent,
            selected: selected
        },
        success: function(response)
            {
                    data = response;
                    table();
            },
        error: function()
        {
            console.log("Error")
        }
    });
}

function table(){
    if(pumpcurrent < max){
        var i = data.length;
        $("#pumpconfiguration").append("<tr class='pumpnumber" + pumpcurrent + "' id='pumpnum" + pumpcurrent + "'><td class='pumpnumber" + pumpcurrent + "'>Select Pump " + pumpcurrent + 
        "</td><td class='pumpnumber" + pumpcurrent + "'><select id='pump" + pumpcurrent + "' name='pump" + pumpcurrent + "'>");
        //This builds the selection option, but it is a little clunky. Can't figure out how to do it in django.forms with the joins that I need to run.
        for(j = 0; j < i; j++){
            $("#pump" + pumpcurrent).append("<option value='" + data[j] + "'>" + data[j] + "</option>");
        }
        $("#pumpnum" + pumpcurrent).append("</select></td><td class='pumpnumber" + pumpcurrent + "'><button type='button' id='pump" + pumpcurrent + "submit' class='buttons' onclick='pumpsubmit(" + 
        pumpcurrent + ")'>Select Pump " + pumpcurrent + "</button></td><td><button type='button' id='modify" + pumpcurrent + "' onclick='modify(" + pumpcurrent + ")' disabled='disabled'>Modify</button></td></tr>");
    }else{
        reservoirs();
    }
}
function pumpsubmit(number){
        selected = $("#pump" + number).val();
        if(selected != "Please choose a different forward pump"){
            pumpcurrent = number + 1;
            for(i=pumpcurrent; i<max; i++){
                $("#pump" + i + "submit").remove();
                $(".pumpnumber" + i).remove();
                $("#pumpnumber" + i).remove();
            }
            //$("#pump" + number).attr("disabled", "disabled");
            //$("#pump" + number + "submit").attr("disabled", "disabled");
            $("#modify" + number).removeAttr("disabled", "disabled");
            $(".flows").html("XXX");
            pumps();
        }
}

$(document).ready(function(){
    $("#modify").click(function(){
        $("button").removeAttr("disabled", "disabled");
        $("select").removeAttr("disabled", "disabled");
        $(".modify").attr("hidden", "hidden");
        $(".modify").attr("disabled", "disabled");
    });
});

function modify(number){
    if(confirm("Are you sure? This will remove all later selections.")){
        pumpcurrent = number+1;
        for(i=pumpcurrent; i<max; i++){
            $("#pump" + i + "submit").remove();
            $(".pumpnumber" + i).remove();
            $("#pumpnumber" + i).remove();
        }
        $("#pump" + number + "submit").removeAttr("disabled", "disabled");
        $("#pump" + number).removeAttr("disabled", "disabled");
        $("#modify" + number).attr("disabled", "disabled");
        $("#reservoirs").empty();
        $("#reservoirconfiguration").attr("hidden", "hidden");
    }else{
        //Pass.
    }    
}

function reservoirs(){
    var pumps = [];
    for(i=1; i<max ; i++){
        pump = $("#pump" + i ).val();
        pumps.push(pump);
    }
    $.ajax({
        url: "manual/reservoirs",
        type: "POST",
        data: {
            csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            pumps: JSON.stringify(pumps)
        },
        success: function(response)
            {
                    flow = response[0];
                    reservoir = response[1];
                    flows();
                    reservoirtable();
            },
        error: function()
        {
            console.log("Error")
        }
    });
}

function flows(){
    $("#flow").html(flow.toFixed(2));
    $("#ninetyfive").html((flow*.95).toFixed(2));
    $("#ninety").html((flow*.9).toFixed(2));
    $("#eightyfive").html((flow*.85).toFixed(2));
    $("#horsepower").html((flow*1.7503/.95).toFixed(2));
}
function reservoirtable(){
    $("#reservoirconfiguration").removeAttr("hidden", "hidden");
    $("#reservoirsubmit").removeAttr("disabled", "disabled");
    for(x in reservoir){
        $("#reservoirs").append("<option value='" + reservoir[x][2] + "'>" + reservoir[x][0] + reservoir[x][1] + "</option>");
    }
}

$(document).ready(function(){
    $("#reservoirsubmit").click(function(){
        //$("#reservoirsubmit").attr("disabled", "disabled");
        //$("#reservoirs").attr("disabled", "disabled");
        
        $.ajax({
            url: "manual/motors",
            type: "POST",
            data: {
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val()
            },
            success: function(response)
                {
                    motor = response;
                    $("#motorconfiguration").removeAttr("hidden", "hidden");
                    motors();
                },
            error: function()
            {
                console.log("Error")
            }
        })
    });
});
function motors(){
    $("#motorconfiguration").removeAttr("hidden", "hidden");
    $("#motorsubmit").removeAttr("disabled", "disabled");
    for(x in motor){
        $("#motors").append("<option value='" + motor[x][2] + "'>" + motor[x][0] + motor[x][1] + "</option>");
    }
}
$(document).ready(function(){
    $("#reservoirmodify").click(function(){
        $("#reservoirsubmit").removeAttr("disabled", "disabled");
        $("#reservoirs").removeAttr("disabled", "disabled");
        $("#motorconfiguration").attr("hidden", "hidden");
    });
});
//Start work on controls options for each pump so I can select actual pump part numbers and pull R9's out of parts database.



var modal;
var img;
var modalImg;
var captionText;

//Just a simple modal picture of the possible through drive option selections.
function modalpic(){
    modal = document.getElementById("myModal");
    img = document.getElementById("myImg");
    modalImg = document.getElementById("img01");
    captionText = document.getElementById("caption");
    var span = document.getElementsByClassName("close")[0];
    img.onclick = function(){
        modal.style.display = "block";
        modalImg.src = this.src;
        captionText.innerHTML = this.alt;
    }
    
    span.onclick = function() { 
    modal.style.display = "none";
  }
}
