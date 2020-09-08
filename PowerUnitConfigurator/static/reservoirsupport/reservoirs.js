var flows = [];
var allreservoirs = [];

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
    var totalvolume = 0;
    for(x in flows){
        volume = ((flows[x] * 1800)/(231*16.3871));
        totalvolume += volume;
        i = Number(x)+1;
        $("#flows").append("Pump " + i + " will flow " + volume.toFixed(2) + " GPM at 1800 RPM. <br>");
    }
    $("#flows").append("Total system flow is " + totalvolume.toFixed(2) + " GPM at 1800 RPM. <br>");
}

function reservoirs(){
    allreservoirs = JSON.parse($("#reservoirs").html());
    console.log(allreservoirs);
}