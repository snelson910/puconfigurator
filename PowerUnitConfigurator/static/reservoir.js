var data;
var accountnumber;

function getdata(){
    data = JSON.parse(JSON.parse($("#data").html()));
    console.log(data[1]);
}