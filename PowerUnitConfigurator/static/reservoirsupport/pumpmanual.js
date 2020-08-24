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
        pumpnum = Number($("#pumpnums").val());
        max = pumpnum + 1;
        pumpcurrent ++;
        if(pumpcurrent <= pumpnum){
            //console.log("Pump number " + pumpcurrent + " function");
            pumps();
        }
        else{
            console.log("Complete");
        }
    })
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
        $("#pumpconfiguration").append("<br><label for='pump" + pumpcurrent + "'>Select Pump " + pumpcurrent + "</label><select id='pump" + pumpcurrent + "' name='pump" + pumpcurrent + "'>");
        for(j = 0; j < i; j++){
            $("#pump" + pumpcurrent).append("<option value='" + data[j] + "'>" + data[j] + "</option>");
        }
        $("#pumpconfiguration").append("</select><button type='button' id='pump" + pumpcurrent + "submit' class='buttons' onclick='pumpsubmit()'>Submit Pump " + pumpcurrent + "</button><br>");
    }else{
        console.log("Completed");
    }
}
function pumpsubmit(){
        selected = $("#pump" + pumpcurrent).val();
        pumpcurrent++;
        pumps();
}

var modal;
var img;
var modalImg;
var captionText;

function setup(){
    modal = document.getElementById("myModal");
    img = document.getElementById("myImg");
    modalImg = document.getElementById("img01");
    captionText = document.getElementById("caption");
    var span = document.getElementsByClassName("close")[0];
    img.onclick = function(){
        //console.log("clicked");
        modal.style.display = "block";
        modalImg.src = this.src;
        captionText.innerHTML = this.alt;
    }
    
    span.onclick = function() { 
    modal.style.display = "none";
  }
}
