var flows = [];

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
    var j = 0;
    for(x in flows){
        i = Number(x) + 1;
        flowhp = (flows[x]*.8322/.95).toFixed(2);
        $("#flows").append("<br>Pump " + i + " will require " + flowhp + " HP at 3000 PSI, 1800 RPM, and 95% efficiency.");
        j += flows[x]
    }
    jhp = (j*.8322/.95).toFixed(2);
    $("#flows").append("<br>Total theoretical required horsepower is " + jhp + " HP at 3000 PSI, 1800 RPM, and 95% efficiency.");
}