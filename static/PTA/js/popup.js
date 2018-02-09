function affirmPopup() {
    var x;
    console.log("hi");
    if (confirm("Are you sure you wish to AFFIRM trade ID XXXXX") == true) {
        x = "You pressed OK!";
        console.log(x);
        socket.send("hi");
    } else {
        x = "You pressed Cancel!";
    }
    //document.getElementById("demo").innerHTML = x;
}

function rejectPopup() {
    var reason = prompt("Reason required for rejecting trade.", "");

    while (reason == ""){
        var reason = prompt("ERROR: Reason not provided. \nReason required for rejecting trade.", "");
    }

   // if (person != null) {
   //     document.getElementById("demo").innerHTML =
   //         "Hello " + person + "! How are you today?";
   // }
}

function callPopup() {
    var x;
    if (confirm("Calling client on xxxx xxx xxxx") == true) {
        x = "You pressed OK!";
    } else {
        x = "You pressed Cancel!";
    }
    //document.getElementById("demo").innerHTML = x;
}

function revertPopup() {
    var reason = prompt("Reason required for reverting trade.", "");

    while (reason == ""){
        var reason = prompt("ERROR: Reason not provided. \nReason required for reverting trade.", "");
    }

    // if (person != null) {
    //     document.getElementById("demo").innerHTML =
    //         "Hello " + person + "! How are you today?";
    // }
}