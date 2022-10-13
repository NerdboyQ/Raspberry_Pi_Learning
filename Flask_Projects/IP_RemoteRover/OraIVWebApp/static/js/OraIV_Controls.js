/*
* This is only used in the html file directly, but it's not necessary
* for the standalone js file.
$(document).ready( function(){
    
//	frame.src = "picar/static/picar/images/test.jpg";
});
*/
var frame = document.getElementById("camFeed_frame");

var control_btns = [
    // rotations
    document.getElementById("rotate_left_btn"),
    document.getElementById("rotate_right_btn"),
    // forward motions
    document.getElementById("diagonal_F_left_btn"),
    document.getElementById("drive_F_btn"),
    document.getElementById("diagonal_F_right_btn"),
    // lateral motions & stop
    document.getElementById("drive_left_btn"),
    document.getElementById("stop_btn"),
    document.getElementById("drive_right_btn"),
    // reverse motions
    document.getElementById("diagonal_R_left_btn"),
    document.getElementById("drive_R_btn"),
    document.getElementById("diagonal_R_right_btn")
    ];

for (i=0;i<control_btns.length;i++){
    control_btns[i].addEventListener("click", handle_control_btn_click);
    console.log("Setting up btns", control_btns[i].id);
}

function handle_control_btn_click(){
    console.log("button clicked: ", this.id);
    fetch(`/drive_cmd/${this.id}`)
    .then(function (response) {
        return response.text();
    }).then(function (text) {
        console.log('GET response text:');
        console.log(text); 
    });
    /*
    $.ajax({
        type: "POST",
        url: "drive_vehicle",
        data:{
            "drive_cmd" : test,
            "csrfmiddlewaretoken":"{{ csrf_token }}",	
        },
        success: function(){
            console.log("success");
        }
    });*/
}