var accountnumber;
var modal;
var img;
var modalImg;
var captionText;
var data;
var data2;
var pumpnum;
var pumpcurrent = 0;
var selected;
var max = 0;
var flow;
var reservoir;
var motor;
var num = 0;

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

//Check cookies and hold account number, will modify to reflect any chosen parts so that they stay stored later on.
function readcookies(){
    var allcookies = document.cookie;
    cookiearray = allcookies.split(';');
    for(x in cookiearray){
        key = cookiearray[x].split('=')[0];
        value = cookiearray[x].split('=')[1];
        if(key.substring(1) == "an"){
            accountnumber = value;
        }
    }
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

function pumps(){
    $.ajax({
        url: "pumpnums",
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

function table(){
    if(pumpcurrent < max){
        var i = data.length;
        $("#pumpconfiguration").append("<tr class='pumpnumber" + pumpcurrent + "' id='pumpnum" + pumpcurrent + "'><td class='pumpnumber" + pumpcurrent + 
        "'>Select Pump " + pumpcurrent + "</td><td class='pumpnumber" + pumpcurrent + "'><select id='pump" + pumpcurrent + "' name='pump" + pumpcurrent + "'>");
        //This builds the selection option, but it is a little clunky. Can't figure out how to do it in django.forms with the joins that I need to run.
        for(j = 0; j < i; j++){
            $("#pump" + pumpcurrent).append("<option value='" + data[j] + "'>" + data[j] + "</option>");
        }
        $("#pumpnum" + pumpcurrent).append("</select></td><td class='pumpnumber" + pumpcurrent + "'><button type='button' id='pump" + pumpcurrent + 
        "submit' class='buttons' onclick='pumpsubmit(" + pumpcurrent + ")'>Select Pump " + pumpcurrent + "</button></td><td><button type='button' id='modify" 
        + pumpcurrent + "' onclick='modify(" + pumpcurrent + ")' disabled='disabled'>Modify</button></td></tr>");
    }else{
        pumpconfig();
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

function pumpconfig(){
    $(".pump").remove();
    pumpparts = []
    var val = num + 1
    pumpparts[0] = $("#pump" + val).val();
    $.ajax({
        url: "pumpselect",
        type: "POST",
        data: {
            csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            pumpparts: JSON.stringify(pumpparts),
            pumpmax: max,
            current: num = 1
        },
        success: function(response)
            {
                    data = response;
                    pumptable();
            },
        error: function()
        {
            console.log("Error")
        }
    });
}

function pumptable(){
    $(".pump").remove();
    $("#pumppref").html(pumpparts[0]);
    $("#notes").removeAttr("hidden", "hidden");
    $("#pumptable").removeAttr("hidden", "hidden");
    var i=0;
    if(data[0][0]=="No pumps with this configuration."){
        $("#pumptable").append("<tr class='pump'><td colspan='8'>No pumps with this configuration.</td></tr>")
    }else{
        for(x in data){
            $("#pumptable").append("<tr class='pump'><td>" + data[i][0] + "</td><td>" + data[i][1] + "</td><td>" + data[i][2] + "</td><td>" + 
            data[i][3] + "</td><td>" + data[i][4] + "</td><td>" + data[i][5] + "</td><td>" + data[i][6] + "</td><td><button onclick='nextpump(" + 
            data[i][0] + ")' >Select</button></td></tr>");
            i++;
        }
    }
}