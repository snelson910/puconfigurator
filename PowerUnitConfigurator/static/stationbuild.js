var spoolCode;
var i = 0;
var stationdata = [];
var station = {}
var voltageAR = [0,0,0,0];
var stations;
var size;
var partNumbers = [];
var stationnum = 1;
var valvenum = [0];
var pressure;
var details;
var searchvalves = [];
//Pull manifold size and number of stations from submitted POST.
$(document).ready(function(){
    var datas = $("#details").html();
	details = JSON.parse(datas);
    size = details[4];
    stations = details[2];
    pressure = details[3];
    $("#stationTag").html("Station " + stationnum);
});
//Disable cables selection if not DIN. Cables will automatically be pushed into partnumbers array.
$(document).ready(function(){
    $("#voltagetype").change(function(){
        if($("#voltagetype").val() == "din"){
            $("#cablesReq").removeAttr("disabled", "disabled");
        }else{
            $("#cablesReq").attr("disabled", "disabled");
        }
    });
});
//Require user to select whether cables are required before submitting.
$(document).ready(function(){
    $("#voltageSubmit").click(function(){
        if($("#stationVoltage").val() != null && $("#voltagetype").val() != null){
            if($("#voltagetype").val() == "din" && $("#cablesReq").val() != null){
                $("#stationMath").removeAttr("hidden", "hidden");
                $(".baseQuestions").attr("hidden", "hidden");
            }else if($("#voltagetype").val() == "conduit"){
                $("#stationMath").removeAttr("hidden", "hidden");
                $(".baseQuestions").attr("hidden", "hidden");
            } 
        }
    });
});
//Highlights the selected spool valve for easier selection process.
$(document).ready(function(){
    $(".spoolButtons").click(function(){
        spoolCode = $(this).attr("value");
        $("#stationSubmit").html("Submit Station " + stationnum + " Valve");
        $("#propsubmit").html("Submit Station " + stationnum + " Valve");
        if(spoolCode != "prop"){
            $("#stationSubmit").removeAttr("hidden", "hidden");
            $("#propsubmit").attr("hidden", "hidden");
        }else{
            $("#propsubmit").removeAttr("hidden", "hidden");
            $("#stationSubmit").attr("hidden", "hidden");
        }
        $(".spoolButtons").css("background-color","white");
        $(this).css("background-color","#d4242c");
    });
});
//Pushes prop valve menu.
$(document).ready(function(){
    $("#propsubmit").click(function(){
        $("#propvalves").removeAttr("hidden", "hidden");
        $("#valveSelection").attr("hidden","hidden");
    });
});
$(document).ready(function(){
    $("#propcancel").click(function(){
        $("#propvalves").attr("hidden", "hidden");
        $("#valveSelection").removeAttr("hidden","hidden");
    });
});
//Proportional valve menu. Will check for valid R9 style number before allowing to proceed.
$(document).ready(function(){
    $("#propSubmit").click(function(){
        var check = document.getElementById("propNum");
        if(!check.checkValidity()) {
            $("#test").html("Invalid?");
        }else{
            valve = $("#propNum").val();
            valve = "R" + valve.slice(-9);
            partNumbers.push(valve);
            valvenum.push(valve);
            partNumbers.push("JHFM-1750");
            if(stationnum < stations){
                stationnum++;
                $("#stationTag").html("Station " + stationnum);
                $("#valveSelection").removeAttr("hidden","hidden");
                $("#propvalves").attr("hidden", "hidden");
                $("#propsubmit").attr("hidden", "hidden");
            }else{
                $("#stationMath").attr("hidden", "hidden");
                $("#sandwichConfig").removeAttr("hidden", "hidden");
                tableBuild()
                $("#configSubmit").removeAttr("hidden", "hidden");
        }
        }
    });
});
//Build spool valve codes based on selections. Limited functionality to cover eighty percent of projects.
$(document).ready(function(){
    $("#stationSubmit").click(function(){
        var voltage = $("#stationVoltage").val();
        var spool = spoolCode;
		if($("#voltagetype").val() == "din"){
        var connect = "N9K4";
		}else{
		var connect = "N9DAL";
        }
        if(spool != "cover" && spool != "cross"){
            switch(true){
                case size == "D03":
                    valve = ("4WE6" + spool + "6X/E" + voltage + connect);
                    searchvalves.push(["4WE6", spool, voltage, connect]);
                    //partNumbers.push(valve);
                    valvenum.push(valve);
                    break;
                case size == "D05":
                    valve = ("4WE10" + spool + "5X/E" + voltage + connect);
                    searchvalves.push(["4WE10", spool, voltage, connect]);
                    //partNumbers.push(valve);
                    valvenum.push(valve);
                    break;
                case size == "D08":
                    if(connect == "N9K4"){
                        connect = "N9ETK4";
                    }else{
                        connect = "N9DA";
                    }
                    valve = ("4WEH22" + spool + "7X/6" + voltage + connect);
                    searchvalves.push(["4WEH22", spool, voltage, connect]);
                    //partNumbers.push(valve);
                    valvenum.push(valve);
                    break;
            }
            if($("#cablesReq").val() == "yes"){    
                if(voltage == "W110" && $("#voltagetype").val() == "din"){
                    if(spool == "D"){
                        partNumbers.push("5J6F4-551-US0A");
                    }else{
                        partNumbers.push("5J6F4-551-US0A");
                        partNumbers.push("5J6F4-551-US0A");
                    }
                }else if(voltage == "G24" && $("#voltagetype").val() == "din"){
                    if(spool == "D"){
                        partNumbers.push("5J6F4-251-US0A");
                    }else{
                        partNumbers.push("5J6F4-251-US0A");
                        partNumbers.push("5J6F4-251-US0A");
                }
                }else if($("#voltagetype").val() == "din" && voltage == "G12" || voltage == "W230"){
                    if(spool == "D"){
                        partNumbers.push("5J6F4-000-US0A");
                    }else{
                        partNumbers.push("5J6F4-000-US0A");
                        partNumbers.push("5J6F4-000-US0A");
                    }
                }else{
                    console.log("Voltage Counter Broken");
                }
            }
        }else{
            //Allow the user to select a cover or crossover plate.
            if(spool == "cover" || spool == "cross"){
                if(spool == "cover"){
                    partNumbers.push(pressure + size + "CPP")
                    valvenum.push(pressure + size + "CPP")
                }
                if(spool == "cross"){
                    partNumbers.push(pressure + size + "COP")
                    valvenum.push(pressure + size + "COP")
                }
            }
        }
        //Checks if all stations have been configured for a directional valve and loops if not yet complete.   
        if(stationnum < stations){
            $("#stationSubmit").attr("hidden", "hidden");
            stationnum++;
            $("#stationTag").html("Station " + stationnum);
        }else{
            $("#stationMath").attr("hidden", "hidden");
            $("#sandwichConfig").removeAttr("hidden", "hidden");
            tableBuild()
            $("#configSubmit").removeAttr("hidden", "hidden");
        }
    });
});
//Loop through the base station table and clone it, changing ID's to allow for later access.
function tableBuild(){
    $("#table").removeAttr("hidden", "hidden");
    if(stations == 1){
        $("#valve1").html(valvenum[1])
    }
    for(j=1; j<stations ; j++){
        $("#table tbody").append($("#table tbody tr:last").clone());
        $("#table tr").each(function(i){ 
            var a = $(this).find('a');
            a.eq(0).html(i);
            a.eq(1).attr('id', 'valve'+i);
            a.eq(1).html(valvenum[i]);
            var select = $(this).find('select');           
            select.eq(0).attr('id', 'floworient0'+i);
            select.eq(1).attr('id', 'flowdirect0'+i);
            select.eq(2).attr('id', 'cbStyle0'+i);
            select.eq(3).attr('id', 'poStyle0'+i);
            select.eq(4).attr('id', 'reduceStyle0'+i);
            select.eq(5).attr('id', 'reduceChecks0'+i);
            select.eq(6).attr('id', 'relievingStyle0'+i);
            i++
        })
    }
}
//Set conditions for each station sandwich valves. Flow controls requires direction, no mixing of reducing valves with or without check valves for simplicity.
$("body").on("click",":input",function(){
    var input = this.id;
    var classes = this.id;
    var valveClass = classes.slice(0,-2);
    if(valveClass.slice(-1) == 0){
        valveClass = classes.slice(0,-3);
    }
    var valveStation = input.slice(-2);
    if(valveStation == "10"){
        valveStation = "010";
    }
    if(valveClass == "floworient"){
        if($("#" + input).val() == "none"){
            $("#flowdirect" + valveStation).attr("disabled", "disabled");
            $("#flowdirect" + valveStation).val("none");
        }else{
            $("#flowdirect" + valveStation).removeAttr("disabled", "disabled");
            $("#flowdirect" + valveStation).val("Meter Out");
        }
    }
    if(valveClass == "reduceStyle"){
        if($("#" + input).val() == "none"){
            $("#reduceChecks" + valveStation).removeAttr("disabled", "disabled");
        }else{
            $("#reduceChecks" + valveStation).attr("disabled", "disabled");
        }
    }
    if(valveClass == "reduceChecks"){
        if($("#" + input).val() == "none"){
            $("#reduceStyle" + valveStation).removeAttr("disabled", "disabled");
        }else{
        $("#reduceStyle" + valveStation).attr("disabled", "disabled");
        }
    }
})
$(document).ready(function(){
    $("#configSubmit").click(function(){
        $(":input").attr("disabled", "disabled");
        $("#sandwichStyleModify").removeAttr("hidden", "hidden");
        $("#sandwichStyleConfirm").removeAttr("hidden", "hidden");
        $("#sandwichStyleModify").removeAttr("disabled", "disabled");
        $("#sandwichStyleConfirm").removeAttr("disabled", "disabled");
        $("#configSubmit").attr("hidden", "hidden");
    });
});
$(document).ready(function(){
    $("#sandwichStyleModify").click(function(){
        $(":input").removeAttr("disabled", "disabled");
        $("#sandwichStyleModify").attr("hidden", "hidden");
        $("#sandwichStyleConfirm").attr("hidden", "hidden");
        $("#configSubmit").removeAttr("hidden", "hidden");
        console.table(searchvalves);
        for(h=0; h<stations;h++){
            var k= h + 1;
            if($("#floworient0" + k).val() == "none"){
                $("#flowdirect0"+ k).attr("disabled", "disabled");
            }
            if($("#reduceStyle0" + k).val() != "none"){
                $("#reduceChecks0" + k).attr("disabled", "disabled");
            }
            if($("#reduceChecks0" + k).val() != "none"){
                $("#reduceStyle0" + k).attr("disabled", "disabled");
            }
        }
    });
});
$(document).ready(function(){
    $("#sandwichStyleConfirm").click(function(){
        $(":input").removeAttr("disabled", "disabled");    
        for(h=0;h<stations;h++){
            var k = h+1;
            console.log(valvenum[k]);
            floworient = $("#floworient0"+k).val();
            if(floworient == "none"){
                floworient = null;
            }
            flowdirect = $("#flowdirect0"+k).val();
            if(flowdirect == "none"){
                flowdirect = null;
            }
            cbStyle = $("#cbStyle0"+k).val();
            if(cbStyle == "none"){
                cbStyle = null;
            }
            poStyle = $("#poStyle0"+k).val();
            if(poStyle == "none"){
                poStyle = null;
            }
            redStyle = $("#reduceStyle0"+k).val();
            if(redStyle == "none"){
                redStyle = null;
            }
            redChecks = $("#reduceChecks0"+k).val();
            if(redChecks == "none"){
                redChecks = null;
            }
            relStyle = $("#relievingStyle0"+k).val();
            if(relStyle == "none"){
                relStyle = null;
            }
            var valve = $("#valve" + k).html();
            station = {
                valveCode: valve,
                floworient: floworient,
                flowdirect: flowdirect,
                cborient: cbStyle,
                poorient: poStyle,
                redorient: redStyle,
                redchecks: redChecks,
                relorient: relStyle
                }
            stationdata.push(station);
                
        }
        console.table(stationdata);
        var data = JSON.stringify(stationdata);
        $("#stationinput").val(data);
        var parts = JSON.stringify(partNumbers);
        $("#partnumbers").val(parts);
        var deets = JSON.stringify(details);
        $("#deets").val(deets);
        var data2 = JSON.stringify(searchvalves);
        $("#search").val(data2);
        $("#formsubmit").submit();
    });
});
