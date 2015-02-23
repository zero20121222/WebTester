init_background();
function init_background(){
	init_localStorage();	
}

//初始化localstorage数据
function init_localStorage() {
	if (localStorage.appName == null) {
		localStorage.appName = "WebTester";
	}

	if(localStorage.testerServer == null){
		localStorage.testerServer = "http://localhost:8888";
	}

	if(localStorage.tester_list == null){
		localStorage.tester_list = JSON.stringify([]);
	}

	if(localStorage.log_result == null){
		localStorage.log_result = JSON.stringify([]);
	}

	if(localStorage.logLevel == null){
		localStorage.logLevel = "log";
	}

	if(localStorage.syncTester == null){
		localStorage.syncTester = "true";
	}
}

var testEngine = null;
//获取测试引擎对象
function get_testerEngine(driver, executePath){
	if(testEngine == null){
		init_testerEngine(driver, executePath);
	}
	return testEngine;
}

//初始化测试引擎
function init_testerEngine(driver, executePath){
	testEngine = chrome.runtime.connectNative('com.tester.client');

	testEngine.onMessage.addListener(function(msg) {
		console.log("WebTester return:" + formatResult(msg));
	});

	testEngine.onDisconnect.addListener(function() {
	  	console.log("WebTester is closed...");
	  	testEngine = null;
	});

	testEngine.postMessage(new EngineDealObj("initEngine", driver, executePath, {}))
}

function sendTester(driver, executePath, testerData){
	sendMessage(new EngineDealObj("testDeal", driver, executePath, testerData));
}

function closeEngine(driver, executePath){
	sendMessage(new EngineDealObj("closeEngine", driver, executePath, {}));
}

function sendMessage(engineObj){
	if(testEngine != null){
		testEngine.postMessage(engineObj);
	}
}

//操作测试引擎的数据格式对象
function EngineDealObj(method, driver, executePath, dataObj){
	//处理方式(initEngine , testDeal)
	this.method = method;
	//引擎类型（chrome, firefox）
	this.driver = driver;
	//引擎地址
	this.execute_path = executePath;

	this.data_obj = dataObj;
}

//测试引擎处理的数据对象
function TesterData(domain, testerAction){
	this.domain = domain;
	this.testerAction = testerAction;
}

function TesterForms(testName, params){
	this.testName = testName;
	this.params = params;
}

function TesterFormData(formType, formElName, formElValue){
	this.formType = formType;
	this.formElName = formElName;
	this.formElValue = formElValue;
}

function TesterActionData(action, elType, elValue, testerResult){
	this.action = action;
	this.elType = elType;
	this.elValue = elValue;
	this.testerResult = testerResult;
}

//测试引擎处理的操作流程
function TesterAction(id, queueId, testNum, urlPath, forms, actionList, sleepTime, waitClose){
	this.id = __default_el(id, null);
	this.queueId = __default_el(queueId, null);
	this.testNum = __default_el(testNum, null);
	this.urlPath = __default_el(urlPath, null);
	this.forms = __default_el(forms, new Array());
	this.actionList = __default_el(actionList, new Array());
	this.sleepTime = __default_el(sleepTime, 2);
	this.waitClose = __default_el(waitClose, 10);
}

//测试处理程序的处理结果
function MessageInfo(m_type, message){
	this.mType = m_type;
	this.message = message;
}

function __default_el(el_in, default_value){
	return el_in == undefined || el_in == null ? default_value : el_in;
}

// 元素对象
var EL_TYPE = {
	id: 1,
	name: 2,
	tag: 3,
	value: 4,
	selector: 5,
	class: 6
}

// 动作元素
var ACTION_TYPE = {
	click: 1,
	doubleClick: 2,
	rightClick: 3,
	mouseOver: 4,
	mouseOut: 5,
	select: 6
}


/********************* engine deal结果 **********************/
function formatResult(msg){
	//记录app的处理结果数据
	var msgObj = new MessageInfo(msg.m_type, msg.message);

	switch(localStorage.logLevel){
		case "log":
			formatLog(msgObj);
			break;

		case "info":
			if(msgObj.mType != "log"){
				formatLog(msgObj);
			}
			break;
		
		case "error":
			if(msgObj.mType == "error" || msgObj.mType == "tResult"){
				formatLog(msgObj);
			}
			break;
		
		case "tResult":
			if(msgObj.mType == "tResult"){
				formatLog(msgObj);
			}
			break;
		default:

	}

	return msgObj;
}

function formatLog(msgObj){
	var logArray = __storage_to_obj(localStorage.log_result);
	logArray.push(msgObj);
	localStorage.log_result = __obj_to_storage(logArray);
}

function cleanLog(){
	localStorage.log_result = JSON.stringify([]);
}


/********************* 数据存储对象 **********************/
function EventObj(tag_name, params){
	this.tagName = tag_name;
	this.params = params;
}

function TesterObj(url , event_obj){
	this.url = url;
	this.events = new Array(event_obj);
}

/*
 * Form: {
	test_type:"form",
	el_name,
	id, 
	class, 
	name, 
	type
 }
 */
chrome.extension.onRequest.addListener(
	function(request, sender, sendResponse) {
		var testers = __storage_to_obj(localStorage.tester_list);
		var req_obj = typeof(request.data) == "object" ? request.data : __storage_to_obj(request.data);

		switch(req_obj.test_type){
			case "form":
				var obj = __tester_obj(testers, sender.tab.url);
				if(obj == null){
					testers.push(new TesterObj(sender.tab.url, new EventObj(req_obj.tagName, req_obj.params)));
				}else{
					obj.events.push(new EventObj(req_obj.tagName, req_obj.params));
				}

				localStorage.tester_list = __obj_to_storage(testers);
				break;
			case "action":
				break;
		}
});

function __tester_obj(testers, url){
	for(var i=0; i<testers.length; i++){
		if(testers[i].url == url){
			return testers[i];
		}
	}

	return null;
}

function __storage_to_obj(local_str){
	return JSON.parse(local_str);
}

function __obj_to_storage(obj){
	return JSON.stringify(obj);
}