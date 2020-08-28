var accountnumber;
function readcookies(){
    var allcookies = document.cookie;
    cookiearray = allcookies.split(';');
    for(x in cookiearray){
        key = cookiearray[x].split('=')[0];
        value = cookiearray[x].split('=')[1];
        if(key.substring(1) == "an"){
            accountnumber = value;
        }
    }
    console.log(accountnumber);
}