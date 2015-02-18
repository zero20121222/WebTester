$(document).ready(function() {
	init_options();

	$("#webDriver").change(function() {
		switch($(this).val()){
			case "chrome":
				setWebDriver("chrome", $(this));
				break;
			case "firefox":
				setWebDriver("firefox", $(this));
				break;
			case "remote":
				setWebDriver("remote", $(this));
				break;
			case "phantomjs":
				setWebDriver("phantomjs", $(this));
				break;
			default:

		}
	});

	$("#save_option").click(function(){
		localStorage.testerServer = $("#testerServer").val();
		localStorage[$("#webDriver").val()] = $("#testerEngine").val();
		localStorage.logLevel = $("#logLevel").val();
		localStorage.syncTester = $("#syncTester").prop("checked");
	});
});

function init_options(){
	$("#testerServer").attr("value", localStorage.testerServer);
	$("#logLevel").val(localStorage.logLevel == "undefined" || null ? "log" : localStorage.logLevel);
	$("#syncTester").attr("checked", localStorage.syncTester == "true");

	setWebDriver($("#webDriver").val(), $("#webDriver"));
}

function setWebDriver(driver , obj){
	var parent_obj = obj.parent();
	parent_obj.children('[name=testerEngine]').remove();
	if(localStorage[driver] == null){
		$("<input type='text' style='width:300px' name='testerEngine' id='testerEngine' placeholder='webDriver path' required/>").appendTo(parent_obj);
	}else{
		$("<input type='text' style='width:300px' name='testerEngine' id='testerEngine' value='"+localStorage[driver]+"' required/>").appendTo(parent_obj);
	}
}

function clearLocalStorage() {
	localStorage.tester_list = JSON.stringify([]);
	setTesterInfo();
}

function deleteCurrentNote() {
	var uuid = $(this).prev().text();
	var object = JSON.parse(localStorage.mynotes);
	delete object[uuid];
	localStorage.mynotes = JSON.stringify(object);
	renderNotes();
}