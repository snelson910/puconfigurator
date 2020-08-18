var valveData;
var details;
var parts;
var search;

function tableBuild(){
    var data = $("#valveData").val();
    valveData = JSON.parse(data);
    var data2 = $("#details").val();
    details = JSON.parse(data2);
    var data3 = $("#partnumbers").val();
    parts = JSON.parse(data3);
    var data4 = $("#search").val();
    search = JSON.parse(data4);
    console.table(search);
    $("#note").append(details[0]);
    $("#confirmationTable").removeAttr("hidden", "hidden");
    var x = (valveData.length);
    var y;
    for(y=0 ; y<x ; y++){
        var stationNum = "station" + y;
        var num = y+1;
        var row = "<tr id=" + stationNum + "><td style='text-align: center;'>" + 
        num + "</td><td>" + 
        valveData[y].valveCode + 
        "</td><td>" + 
        valveData[y].floworient + 
        "</td><td>" + 
        valveData[y].flowdirect + 
        "</td><td>" +
        valveData[y].cborient + 
        "</td><td>" +
        valveData[y].poorient +
        "</td><td>" +
        valveData[y].redorient +
        "</td><td>" + 
        valveData[y].redchecks +
        "</td><td>" + 
        valveData[y].relorient + 
        "</td>;"
        $("#tbody").append(row);
    }

    $("#configurationTable td").each(function(){
        if($(this).html() == "null"){
            $(this).html("");
        }
    })
    var counts = {};
    $(document).ready(function(){
        parts.forEach(function(x) {  counts[x] = (counts[x] || 0) +1;});
        for(i=0, keys = Object.keys(counts), len = keys.length; i<len; i++){
            $("#bom").append("<tr><td style='text-align: center;'>" + counts[keys[i]] + "</td><td>" + keys[i] + "</td></tr>")
        }
    });
}
