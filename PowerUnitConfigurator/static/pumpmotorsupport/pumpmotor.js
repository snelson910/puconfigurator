var data;
var data2;
$(document).ready(function(){
    $("#submit").click(function(){
        //An attempt at form validation.
        if($("#id_motor-0-hp").val() == ""){
            $("#id_motor-0-hp").css("background-color","yellow")
        }else{
            $("#id_motor-0-hp").css("background-color","white")
        }
        if($("#id_pump-0-pumps").val() == ""){
            $("#id_pump-0-pumps").css("background-color","yellow")
        }else{
            $("#id_pump-0-pumps").css("background-color","white") 
        }
        if($("#voltage").val() == ""){
            $("#voltage").css("background-color","yellow")
        }else{
            $("#voltage").css("background-color","white") 
        }
        if($("#id_motor-0-hp").val() == "" || $("#id_pump-0-pumps").val() == "" || $("#voltage").val() == ""){}else{
            coupling();
        }
    });
});
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

function coupling(){
    $.ajax({
        url: "pumpmotor/coupling",
        type: "POST",
        data: {
            csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            horsepower: $("#id_motor-0-hp").val(),
            pump: $("#id_pump-0-pumps").val(),
            voltage: $("#voltage").val()
        },
        success:function(response)
        {
            if(response != "0"){
                $("#error").attr("hidden", "hidden");
                data = response;
                tablebuild();
            }else{
                $("#table").attr("hidden", "hidden");
                $("#error").removeAttr("hidden", "hidden");
                $("#error").html("Motor option not found");
            }
        }
    });
}
function tablebuild(){
    $("#bellhousing").html(data[0]);
    $("#motcoup").html(data[1]);
    $("#pumcoup").html(data[2]);
    $("#shafts").html(data[3] + " inches");
    $("#motor").html(data[4]);
    $("#pump").html(data[5]);
    $("#insert").html(data[6]);
    $("table").removeAttr("hidden", "hidden")
    $("#data").val(JSON.stringify(data));
}
$(document).ready(function(){
    $("#reservoirselect").click(function(){
        reservoir();
    });
});
function reservoir(){
    $.ajax({
        url: "reservoir",
        type: "POST",
        data: {
            csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            data1: $("#data").val()
        },
        success:function(response)
        {
            if(response != ""){
                $("#motorselection").attr("hidden", "hidden");
                $("#reservoirselection").removeAttr("hidden", "hidden");
                $("#flow").html(response.flow);
                $("#recommended").html(response.recommended);
            }else{
                console.log("Not Working")
            }
        }
    });
}

$(document).ready(function(){
    $("#reservoirsubmit").click(function(){
        data.push($("#id_reservoir_size-0-reservoirs").val())
        console.log("Reservoir number is " + data[6]);
        $("#formdata").val(JSON.stringify(data));
        console.log($("#formdata").val());
    });
});