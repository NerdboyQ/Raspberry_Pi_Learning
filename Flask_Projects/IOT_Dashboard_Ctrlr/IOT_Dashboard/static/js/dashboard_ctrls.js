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
function scan_for_bt_devices() {
	bt_rst_btn.firstChild.textContent = 'bluetooth_searching';
	console.log("Scanning for bt devices...");
	bt_device_list.innerHTML = '<div class=\'loader\'></div>';
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
			var _btBtn = document.createElement("a");
			_btBtn.setAttribute("class", "btn btCtl");
			_btBtn.setAttribute("id", "btConnectBtn");
			var _btIcon = document.createElement("i");
			_btIcon.setAttribute("class", "material-icons");
			li.appendChild(textNode);
			li.appendChild(_btBtn);
			_btIcon.appendChild(document.createTextNode("bluetooth_disabled"));
			_btBtn.appendChild(_btIcon);
			_btBtn.setAttribute("style", "margin-left:auto;margin-right:0;");
			_btBtn.setAttribute("id", json["bt_devices"][i]["name"]);
			_btBtn.addEventListener("click", bt_connect);
			console.log(json["bt_devices"][i]);
			c+=1;
		}

		bt_rst_btn.firstChild.textContent = 'settings_bluetooth'; 	
	});
}

function bt_connect(){
	console.log("attempting bt connect for " + this.id);
	fetch('/bt_connect/' + this.id)
	.then(function (response) {
		return response.json();
	}).then (function (json){
		console.log(json);
	});
}
