/*$(document).ready(function(){
    $("#submit").click(function(){
        var value = document.getElementById("text");
        if(value.checkValidity()) {
            $("#test").html("Invalid?");
        }else{
            $("#test").html("Valid?");
        }

    });
});*/
var partNumbers = [
    "Part 1",
    "Part 2",
    "Part 3",
    "Part 4",
    "Part 1",
    "Part 6",
    "Part 4",
    "Part 5",
    "Part 9",
    "Part 2",
    "Part 2",
    "Part 1",
    "Part 7",
    "Part 7",
    "Part 5",
    "Part 5"
];
$(document).ready(function(){
    $("#submit").click(function(){
        var len = partNumbers.length;
        var id;
        for(i=0;i<len;i++){
            id="valve" + i;
            $("#" +id).html(partNumbers[i]);
        }
    });
});

var counts = {};
$(document).ready(function(){
    partNumbers.forEach(function(x) {  counts[x] = (counts[x] || 0) +1;});
    for(i=0, keys = Object.keys(counts), len = keys.length; i<len; i++){
        $("#bom").append("<tr><th>" + keys[i] + "</th><th>" + counts[keys[i]] + "</th></tr>")
    }
});

var num=3;/*
$(document).ready(function(){
    $("#submit").click(function(){
        for(j=1; j<num ; j++){
        $("#bom tbody").append($("#bom tbody tr:last").clone());
        $("#bom tr").each(function(i){ 
            var a = $(this).find('a');
            a.eq(0).attr('id', 'row'+i);
            a.eq(0).html(partNumbers[i]);
            var select = $(this).find('select');           
            select.eq(0).attr('id', 'flowStyle'+i);
            select.eq(1).attr('id', 'fcDirect'+i);
            select.eq(2).attr('id', 'relievingStyle'+i);
            select.eq(3).attr('id', 'poStyle'+i);
            select.eq(4).attr('id', 'reduceStyle'+i);
            select.eq(5).attr('id', 'reduceChecks'+i);
            select.eq(6).attr('id', 'relievingStyle'+i);
            i++
        })
        }
        console.log("BUILDING TABLE");
        
    for(j=0; j<3 ; j++){
        console.log("TEST"+j);
        $("#valvetable tbody").append($("#bom tbody tr:last").clone());
        $("#valvetable tr").each(function(i){
            i++
            k = i+1;
            var a = $(this).find('a');
            a.eq(0).attr("id", 'row'+i);
            a.eq(0).html(i);
            var select = $(this).find("select");           
            select.eq(0).attr("id", "flowStyle"+k);
            select.eq(1).attr("id", "fcDirect"+k);
            console.log(select.eq());
            select.eq(2).attr("id", "cbStyle"+k);
            select.eq(3).attr("id", "poStyle"+k);
            select.eq(4).attr("id", "reduceStyle"+k);
            select.eq(5).attr("id", "reduceChecks"+k);
            select.eq(6).attr("id", "relievingStyle"+k);
        })
    }*/
    /*});
});*/

