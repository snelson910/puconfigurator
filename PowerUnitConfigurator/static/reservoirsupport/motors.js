var flows = [];
var pumpflows = [];
var pumphp = [];
var motor = [];

function cookiecheck(){
    var ac = document.cookie;
    ca = ac.split(';');
    for(x in ca){
        key = ca[x].split('=')[0];
        value = ca[x].split('=')[1];
        if(key == " flows"){
            flows = JSON.parse(value);
            flowcalc();
        }
    }
}

function flowcalc(){
    $("#flow_div").removeAttr("hidden", "hidden");
    var j = 0;
    for(x in flows){
        i = Number(x) + 1;
        $("#flows").append("<br>Pump " + i + " Pressure: <input type='number' id='pump" + i + "'><input type='button' onclick='flow(" + i + ")' value='Submit'><br><a id='hp" +
        i + "'>0</a> HP, 1800 RPM, 95% efficiency.");
    }
}

function flow(i){
    var j = i-1;
    var pressure = $("#pump" + i).val();
    var pumpflow = flows[j];
    var horsepower = (((pressure*pumpflow)*.4755)/1714)/.95;
    $("#hp" + i).html(horsepower.toFixed(2));
    pumphp[j] = horsepower;
    var total = 0;
    for(x in pumphp){
        total = total + pumphp[x];
    }
    $("#total").html("Total theoretical required horsepower is " + total.toFixed(2) + " HP at 1800 RPM and 95% efficiency.");
}

function motors(){
    motor = JSON.parse($("#allmotors").html());
    for(x in motor){
        $("#motorselect").append("<option value='" + x + "'>"+ motor[x][0] + " HP, " + motor[x][1] + "</option>");
    }
}

$(document).ready(function(){
    $("#motorsubmit").click(function(){
        var motornumber = $("#motorselect").val();
        var selection = motor[motornumber][3];
        document.cookie="motor=" + selection + ";SameSite=Lax; Secure; path=/";
        console.log(document.cookie);
        window.location.replace("/newunit/manual");
    });
});
    