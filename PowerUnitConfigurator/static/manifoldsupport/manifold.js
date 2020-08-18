"use strict";
var manifoldPN;
var reliefPN;
var valvePN;
var voltageAR = [0,0,0,0];
var details = {};

$(document).ready(function(){
	$("#sizeSubmit").click(function(){
		var valveS;
		var reliefS;
		var pressS;
		var relS;
		if($("#valveSize").val() == null){
			valveS = "1";
			$("#valveSize").css("background-color","yellow");
		}else{
			$("#valveSize").css("background-color","white");
		}
		if($("#reliefSelect").val() == null){
			reliefS = "1";
			$("#reliefSelect").css("background-color","yellow");
		}else{
			$("#reliefSelect").css("background-color","white");
		}
		if($("#pressureSelect").val() == null){
			pressS = "1"
			$("#pressureSelect").css("background-color","yellow");
		}else{
			$("#pressureSelect").css("background-color","white");
		}
		if($("#reliefSelect").val() == "1" && $("#reliefStyle").val() == null){
			relS = "1";
			$("#reliefStyle").css("background-color","yellow");
		}else{
			$("#reliefStyle").css("background-color","white");
		}
		if(valveS == "1" || reliefS == "1" || pressS == "1" || relS == "1"){
			alert("Please complete the form.");
		}else{
			reliefMath();
		}
	});
});

//Show or hide the relief valve style dropdown dependant on yes/no valve choice.
$(document).ready(function(){
	$("#reliefSelect").change(function(){
		if($("#reliefSelect").val() == "1")
			{
			$(".reliefClass").removeAttr("hidden");
			}else{
			$(".reliefClass").attr("hidden","hidden");
			}
		});
	});
		
	//Select standard, stock JHF relief valve dependant on selected style and size.
function reliefMath(){
	var rPressure = $("#pressureSelect").val();
	var rStyle = $("#reliefStyle").val();
	var rSize = $("#valveSize").val();
	if(rPressure == ""|| rStyle == "" || rSize == ""){
		$("#reliefValve").html("");
		}else if($("#reliefSelect").val() == "0"){
			$("#reliefValve").html("");
		}else{
			switch(true){
				case rSize == "D03":
					if(rStyle == "direct" && rPressure == "lowPressure"){
						reliefPN = "RDDA-LAN";
						$("#reliefValve").html("Relief valve:<br>RDDA-LAN");
					}else if(rStyle == "direct" && rPressure == "highPressure"){
						reliefPN = "RDDA-LCN";
						$("#reliefValve").html("Relief valve:<br>RDDA-LCN");
					}else if(rStyle == "pilot" && rPressure == "lowPressure"){
						reliefPN = "RPEC-LAN";
						$("#reliefValve").html("Relief valve:<br>RPEC-LAN");
					}else if(rStyle == "pilot" && rPressure == "highPressure"){
						reliefPN = "RPEC-LCN";
						$("#reliefValve").html("Relief valve:<br>RPEC-LCN");
					}
					break;
				case rSize == "D05":
				case rSize == "D08":
					if(rStyle == "direct" && rPressure == "lowPressure"){
						reliefPN = "RDFA-LAN";
						$("#reliefValve").html("Relief valve:<br>RDFA-LAN");
					}else if(rStyle == "direct" && rPressure == "highPressure"){
						reliefPN = "RDFA-LCN";
						$("#reliefValve").html("Relief valve:<br>RDFA-LCN");
					}else if(rStyle == "pilot" && rPressure == "lowPressure"){
						reliefPN = "RPGC-LAN";
						$("#reliefValve").html("Relief valve:<br>RPGC-LAN");
					}else if(rStyle == "pilot" && rPressure == "highPressure"){
						reliefPN = "RPGC-LCN";
						$("#reliefValve").html("Relief valve:<br>RPGC-LCN");
					}
					break;
				}
			}
		manifoldMath();
	}

	//Combines characters to result in Daman part number for bar manifolds, parallel only, with SAE ports.
function manifoldMath()
{	
	var size = $("#valveSize").val();
	var stations;
	var reliefnum;
	var pressure;
	var spacing;
	if($("#reliefSelect").val() == "1"){
		reliefnum = "/S";
	}else if($("#reliefSelect").val() == "0"){
		reliefnum = "";
	}
	if($("#pressureSelect").val() == "highPressure"){
		pressure = "D";
	}else{
		pressure = "A";
	}
	if($("#stationNumber").val() < 10){
		stations = "0" + $("#stationNumber").val();
	}else{
		stations = $("#stationNumber").val();
	}
	if(size == "D03"){
		spacing = "2";
		$("#manisize").val("3");
	}else if(size == "D05"){
		spacing = "3";
		$("#manisize").val("5");
	}else if(size == "D08"){
		spacing = "5";
		$("#manisize").val("8");
	}
	manifoldPN = pressure + size + "P" + stations + spacing + "S" + reliefnum;
	$("#manifold").html("Manifold: <br>" + manifoldPN);
	$("#stationMath").removeAttr("hidden", "hidden");
	$("#sizeSelect").attr("hidden", "hidden");
	$("#maniConfirm").removeAttr("hidden", "hidden");
	$("#maniModify").removeAttr("hidden", "hidden");
	$(".confirmClass").removeAttr("hidden", "hidden");
	$("#maniNum").html(manifoldPN);
	$("#manifoldnum").val(manifoldPN);
	$("#stationnum").val($("#stationNumber").val());
	if(reliefPN == ""){
		$("#reliefNum").html("None");
		$("#reliefvalvenum").val("");
	}else{
		$("#reliefNum").html(reliefPN);
		$("#reliefvalvenum").val(reliefPN);
	}
	details[0] = $("#projectid").html();
	details[1] = manifoldPN;
	details[2] = stations;
	details[3] = pressure;
	details[4] = size;
	details[5] = reliefPN;
	var detail = JSON.stringify(details);
	$("#details").val(detail);
}
	
$(document).ready(function(){
	$("#maniModify").click(function(){
		$("#sizeSelect").removeAttr("hidden", "hidden");
		$("#stationMath").attr("hidden", "hidden");
		$("#maniConfirm").attr("hidden", "hidden");
		$(".confirmClass").attr("hidden", "hidden");
		reliefPN = "";
		$("#maniNum").html("");
		$("#reliefNum").html("");
		$("#manifold").html("");
		$("#reliefValve").html("");
	})
})