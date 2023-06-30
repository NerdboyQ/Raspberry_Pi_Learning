var bt_scan_btn = document.getElementById("bt_scan_btn");
var bt_rst_btn = document.getElementById("bt_rst_btn");
var bt_device_lst = document.getElementById("bt_device_list");
bt_scan_btn.addEventListener("click", scan_for_bt_devices);
bt_rst_btn.addEventListener("click", reset_bt);


function reset_bt(){
    console.log("Restting Bluetooth Service...");
    fetch("/bt_rst")
    .then(function (response){
      return response.json();  
    }).then(function (json) {
        console.log(json);
    });
}
function scan_for_bt_devices(){
	console.log("Scanning for bt devices...");
	fetch('/bt_scan')
	.then(function (response) {
		return response.json();
	}).then(function (json) {
		console.log('GET response text:');
		console.log(json);
		var c = 0;
		bt_device_list.innerHTML = '';
		for (var i in json["bt_devices"]){
			var li = document.createElement("li");
			var textNode = document.createTextNode(json["bt_devices"][i]["name"]);
			li.setAttribute("id", "btDev_" + c);
			li.setAttribute("class", "btDevRow");
			bt_device_list.appendChild(li);
			li.appendChild(textNode);
			console.log(json["bt_devices"][i]);
			c+=1;
		}
	});
}
