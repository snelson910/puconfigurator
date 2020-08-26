var data;
var data2;
var pumpnum;
var pumpcurrent = 0;
var selected = "";
var max = 0;
/* Not yet functional; will add back in once I get to the motor selection portion.
$(document).ready(function(){
    $("#id_motor-0-hp").change(function(){
        //Try to force the user to make good valid motor selections. Can't get the JS to drop the horsepower selection, though...
        if($("#id_motor-0-hp").val() > 5){
            $("#1").attr("disabled", "disabled");
        }else{
            $("#1").removeAttr("disabled", "disabled");
        }
        if($("#id_motor-0-hp").val() < 1 || $("#id_motor-0-hp").val() > 40){
            $("#3").attr("disabled", "disabled");
        }else{
            $("#3").removeAttr("disabled", "disabled");
        }
    })
});
*/
$(document).ready(function(){
    $("#pumpnumsubmit").click(function(){
        $("#pumpnumsubmit").attr("disabled", "disabled");
        $("#pumpnums").attr("disabled", "disabled");
        $("#pumpnummodify").removeAttr("disabled","disabled");
        pumpnum = Number($("#pumpnums").val());
        max = pumpnum + 1;
        pumpcurrent ++;
        if(pumpcurrent <= pumpnum){
            //console.log("Pump number " + pumpcurrent + " function");
            console.log("Working1");
            pumps();
        }
        else{
            console.log("Complete");
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
            //pumps();
            $("#pumpnums").removeAttr("disabled", "disabled");
            $("#pumpnumsubmit").removeAttr("disabled", "disabled");
            $("#pumpnummodify").attr("disabled","disabled");
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
        pumpcurrent + ")'>Submit Pump " + pumpcurrent + "</button></td><td><button type='button' id='modify" + pumpcurrent + "' onclick='modify(" + pumpcurrent + ")' disabled='disabled'>Modify</button></td></tr>");
    }else{
        console.log("Completed");
    }
}
function pumpsubmit(number){
        selected = $("#pump" + number).val();
        //console.log(number);
        pumpcurrent = number + 1;
        for(i=pumpcurrent; i<max; i++){
            $("#pump" + i + "submit").remove();
            $(".pumpnumber" + i).remove();
            $("#pumpnumber" + i).remove();
        }
        /*console.log("Number = " + number);
        console.log("Pumpnums = " + pumpnum);*/
        $("#pump" + number).attr("disabled", "disabled");
        $("#pump" + number + "submit").attr("disabled", "disabled");
        $("#modify" + number).removeAttr("disabled", "disabled");
        pumps();
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
    }else{
        //Pass.
    }    
}








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
