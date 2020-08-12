var spoolCode;
var data;
var details;
var spoolValveCodes = [];
var i = 0;
var stationdata = [];
var station = {}
var voltageAR = [0,0,0,0];
var stations = $("#spoolnumber").html();
var size;
var stationNum;
var valve;
$(document).ready(function(){
	data = $("#details").html();
	details = JSON.parse(data);
	stationNum = details[2];
	size = details[4];
});
$(document).ready(function(){
	$(".spoolButtons").click(function(){
		spoolCode = $(this).attr("value");
		if(spoolCode == "prop"){
			$("#valveVoltage").attr("hidden", "hidden");
			$(".spoolButtons").css("background-color","white");
			$(this).css("background-color","#d4242c");
			$("#voltageSubmit").removeAttr("hidden", "hidden");
			$("#voltageSubmit").removeAttr("disabled", "disabled");
		}else{
			$(".spoolButtons").css("background-color","white");
			$(this).css("background-color","#d4242c");
			$("#valveVoltage").removeAttr("hidden", "hidden");
			$("#voltageSubmit").attr("hidden", "hidden");
		}
	});
});
$(document).ready(function(){
	$("#stationVoltage").on("change",function(){
		$("#voltageSubmit").removeAttr("disabled", "disabled");
		$("#voltageSubmit").removeAttr("hidden", "hidden");
	});
	$("#voltagetype").on("change",function(){
		$("#voltageSubmit").removeAttr("disabled", "disabled");
		$("#voltageSubmit").removeAttr("hidden", "hidden");
	});
});
$(document).ready(function(){
	$("#voltageSubmit").click(function(){
		var voltage = $("#stationVoltage").val();
		if($("#voltagetype").val() == "din"){
		var connect = "N9K4";
		}else{
		var connect = "N9DAL";
		}
		if(spoolCode == "prop"){
			switch(true){
				case size == 3:
					$("#4WRZ").attr("disabled", "disabled");
					$("#4WRZE").attr("disabled", "disabled");
					$("#4WRH").attr("disabled", "disabled");
					break;
				case size == 5:
				case size == 8:
					$("#4WRA").attr("disabled", "disabled");
					$("#4WRAE").attr("disabled", "disabled");
					$("#4WRE").attr("disabled", "disabled");
					$("#4WREE").attr("disabled", "disabled");
					$("#4WREEM").attr("disabled", "disabled");
					break;
				}
			voltageAR[3]++;
			$("#propvalves").removeAttr("hidden", "hidden");
			$("#valveSelection").attr("hidden","hidden");
		}else{
			if(voltage == null || connect == null){
			console.log("BREAK");
			}else{
				var spool = spoolCode;
				switch(true){
					case size == "D03":
						valve = ("4WE6" + spool + "6X/E" + voltage + connect);
						spoolValveCodes.push(valve);
						console.log(valve);
						break;
					case size == "D05":
						valve = ("4WE10" + spool + "5X/E" + voltage + connect);
						spoolValveCodes.push(valve);
						console.log(valve);
						break;
					case size == "D08":
						if(connect == "N9K4"){
							connect = "N9ETK4";
						}else{
							connect = "N9DA";
						}
						valve = ("4WEH22" + spool + "7X/6" + voltage + connect);
						spoolValveCodes.push(valve);
						console.log(valve);
						break;
				}
					
				if(voltage == "W110"){
					if(spool == "D"){
						voltageAR[0] += 1;
					}else{
						voltageAR[0] += 2;
					}
				}else if(voltage == "G24"){
					if(spool == "D"){
						voltageAR[1] += 1;
					}else{
						voltageAR[1] += 2;
					}
				}else if(voltage == "G12" || voltage == "W230"){
					if(spool == "D"){
						voltageAR[2] += 1;
					}else{
						voltageAR[2] += 2;
					}
				}else{
					console.log("Voltage Counter Broken");
				}
				//console.table(voltageAR)
				$("#valveSelection").attr("hidden","hidden");
				$("#sandwichTime").removeAttr("hidden", "hidden");
			}
		}
	});
});
$(document).ready(function(){
	$("#propSubmit").click(function(){
		voltageAR[3] += 1
		$("#sandwichTime").removeAttr("hidden", "hidden");
		$("#propvalves").attr("hidden", "hidden");
	});
});
$(document).ready(function(){
	$("#flowControl").change(function(){
		if($("#flowControl").is(":checked")){
			$(".flowControlConfig").removeAttr("hidden", "hidden");
		}else{
			$(".flowControlConfig").attr("hidden", "hidden");
		}
	});
});
$(document).ready(function(){
	$("#counterBalance").change(function(){
		if($("#counterBalance").is(":checked")){
			$(".counterbalanceConfig").removeAttr("hidden", "hidden");
		}else{
			$(".counterbalanceConfig").attr("hidden", "hidden");
		}
	});
});
$(document).ready(function(){
	$("#poCheck").change(function(){
		if($("#poCheck").is(":checked")){
			$(".pocheckConfig").removeAttr("hidden", "hidden");
		}else{
			$(".pocheckConfig").attr("hidden", "hidden");
		}
	});
});
$(document).ready(function(){
	$("#reducing").change(function(){
		if($("#reducing").is(":checked")){
			$(".reducingConfig").removeAttr("hidden", "hidden");
			$("#reducingCheck").attr("disabled", "disabled");
		}else{
			$(".reducingConfig").attr("hidden", "hidden");
			$("#reducingCheck").removeAttr("disabled", "disabled");
		}
	});
});
$(document).ready(function(){
	$("#reducingCheck").change(function(){
		if($("#reducingCheck").is(":checked")){
			$(".reducingCheckConfig").removeAttr("hidden", "hidden");
			$("#reducing").attr("disabled", "disabled");
		}else{
			$(".reducingCheckConfig").attr("hidden", "hidden");
			$("#reducing").removeAttr("disabled", "disabled");
		}
	});
});
$(document).ready(function(){
	$("#relieving").change(function(){
		if($("#relieving").is(":checked")){
			$(".relievingConfig").removeAttr("hidden", "hidden");
		}else{
			$(".relievingConfig").attr("hidden", "hidden");
		}
	});
});
$(document).ready(function(){
	$("#sandwichStyleSubmit").click(function(){
		$(".sandwichConfigurator").attr("disabled", "disabled");
		$("#sandwichStyleSubmit").attr("hidden", "hidden");
		$(".configConfirm").removeAttr("hidden","hidden");
		$(".configConfirm").removeAttr("disabled", "disabled");
		var	flowDirect = "N/A";
		var flowStyle = "N/A";
		var cbStyle= "N/A";
		var poStyle = "N/A";
		var redStyle = "N/A";
		var redChecks = "N/A";
		var relStyle = "N/A";
		if($("#flowControl").is(":checked") == true){
			flowDirect = $("#fcDirect").val();
			flowStyle = $("#flowStyle").val();
		}else{
			flowDirect = "N/A";
			flowStyle = "N/A";
		}
		if($("#counterBalance").is(":checked") == true){
			cbStyle = $("#cbStyle").val();
		}else{
			cbStyle = "N/A";
		}
		if($("#poCheck").is(":checked") == true){
			poStyle = $("#poStyle").val();
		}else{
			poStyle = "N/A";
		}
		if($("#reducing").is(":checked") == true){
			redStyle = $("#reduceStyle").val();
			redChecks = "N/A";
		}else{
			redStyle = "N/A";
		}
		if($("#reducingCheck").is(":checked") == true){
			redChecks = $("#reduceChecks").val();
			redStyle = "N/A";
		}else{
			redChecks = "N/A";
		}
		if($("#relieving").is(":checked") == true){
			relStyle = $("#relievingStyle").val();
		}else{
			relStyle = "N/A";
		}
		station = {
			valveCode: valve,
			floworient: flowStyle,
			flowdirect: flowDirect,
			cborient: cbStyle,
			poorient: poStyle,
			redorient: redStyle,
			redchecks: redChecks,
			relorient: relStyle
			}
	});
});
$(document).ready(function(){
	$("#sandwichStyleModify").click(function(){
		$(".sandwichConfigurator").removeAttr("disabled", "disabled");
		$(".configConfirm").attr("hidden", "hidden");
		$("#sandwichStyleSubmit").removeAttr("hidden", "hidden");
	});
});
$(document).ready(function(){
	$("#sandwichStyleConfirm").click(function(){
		cleanUp();
	});
});

function cleanUp(){
	$("#sandwichTime").attr("hidden", "hidden");
	$(".spoolButtons").css("background-color","white");
	$(".cleanupClass").attr("hidden", "hidden");
	$(".sandwichConfigurator").removeAttr("disabled", "disabled");
	$(".configConfirm").attr("hidden", "hidden");
	$("#sandwichStyleSubmit").removeAttr("hidden", "hidden");
	$("#voltageSubmit").attr("hidden", "hidden");
	$(".cleanupClass")[0].reset();
	stationdata.push(station);
	console.log(stationdata[0].floworient);
	i=i+1;
	if(i < (stationNum)){
		cycle();
	}else{
		var data = JSON.stringify(stationdata);
		$("#stationinput").val(data);
		$("#valveData").val(stationdata);
		var voltagedata = JSON.stringify(voltageAR);
		$("#voltages").val(voltagedata);
		var manidetails = JSON.stringify(details);
		$("#detailsinput").val(manidetails);
		document.stationsubmit.submit();
	}
}
function cycle(){
	$("#stationMath").removeAttr("hidden", "hidden");
	$("#valveSelection").removeAttr("hidden", "hidden");
	var stationNum = i + 1;
	$("#stationTag").html("Station " + stationNum);
}