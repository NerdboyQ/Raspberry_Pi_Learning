var bt_scam_btn = document.getElementById("bt_scan_btn");

bt_scan_btn.addEventListener("click", scan_for_bt_devices);

function scan_for_bt_devices(){
	console.log("Scanning for bt devices...");
	fetch('/bt_scan')
	.then(function (response) {
		return response.text();
	}).then(function (text) {
		console.log('GET response text:');
		console.log(text);
	});
}
