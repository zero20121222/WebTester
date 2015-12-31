var back_env = chrome.extension.getBackgroundPage();

$(document).ready(function() {

	$("#content").find("[id^='tab']").hide(); // Hide all content
    $("#tabs li:first").attr("id","current"); // Activate the first tab
    $("#content #tab1").fadeIn(); // Show first tab's content
    
    $('#tabs a').click(function(e) {
        e.preventDefault();
        if ($(this).closest("li").attr("id") == "current"){ //detection for current tab
         return;       
        }
        else{             
          $("#content").find("[id^='tab']").hide(); // Hide all content
          $("#tabs li").attr("id",""); //Reset id's
          $(this).parent().attr("id","current"); // Activate this
          $('#' + $(this).attr('name')).fadeIn(); // Show content for the current tab
        }
    });

    //set tester engine with options value
    setInitValue();

    $("#btn_clean").click(function(){
    	clearLocalStorage();
    });

    $("#save_option").click(function(){
    	localStorage.testerServer = $("#testerServer").val();
    });

    $("#btn_commit").click(function(){
        sendMessage();

    	if(localStorage.syncTester == "true"){
            $('.theme-popover-mask').fadeIn(100);
            $('#sync_tester').slideDown(200);

            setSearchQueue();
    	}
    });

    $('.close').click(function(){
        $('.theme-popover-mask').fadeOut(100);
        $('#sync_tester').slideUp(200);
    });

    //同步测试数据到server端
    $('#save_tester').click(function(){
        syncTesterInfo();

        $('.theme-popover-mask').fadeOut(100);
        $('#sync_tester').slideUp(200);
    });

    $("#close_engine").click(function(){
    	back_env.closeEngine(engine_value.text(), engine_value.val());
    });

    $("#log_clean").click(function(){
    	$("#app_log_list").empty();
    	back_env.cleanLog();
    });

	setTesterInfo();
	setTesterLog();
});

function sendMessage(){
    var engine_value = $("#testerEngine");
	var engine = back_env.get_testerEngine(engine_value.text(), engine_value.val());

    var tester_data = formatTesterData();
	back_env.sendTester(engine_value.text(), engine_value.val(), tester_data);

    initSyncNames(tester_data);

	var syncTester = JSON.parse(localStorage.needSyncTester);
	syncTester.push(tester_data);
    localStorage.needSyncTester = JSON.stringify(syncTester);
}

function initSyncNames(testerData){
    var testerLi = $("#testerNameL").children();

    //删除子元素
    for(var i=1; i<testerLi.length; i++){
        $(testerLi[i]).remove();
    }

    var idNum = null;
    for(var key in testerData.testerAction){
        idNum = Number(key) + 1;
        $("<li><label for='testerName"+idNum+"'>TesterName"+idNum+":</label><input type='text' name='testerName"+idNum+"' id='testerName"+idNum+"'/></li>").appendTo($("#testerNameL"));
    }
}

function syncTesterInfo(){
    var testerLi = $("#testerNameL").children();

    var nameList = new Array();
    for(var i=1; i<testerLi.length; i++){
        nameList.push($($(testerLi[i]).children("[type=text]")[0]).val());
    }

    var ifSet = false;
    for(var key in nameList){
        if(nameList[key] != null && nameList[key] != ""){
            ifSet = true;
        }
    }

    if(ifSet){
        var syncTester = JSON.parse(localStorage.needSyncTester);
        var testerGroup = syncTester.pop();

        var testQueue = Number($("#testQueue").val());

        var actionList = testerGroup.testerAction;
        for(var key in actionList){
            actionList[key]["queueId"] = testQueue;

            for(var key1 in actionList[key]["forms"]){
                actionList[key]["forms"][key1]["testName"] = nameList[key];
            }
        }

        console.log(testerGroup);

        $.ajax({
            type : 'POST',
            contentType : 'application/json',
            url : localStorage.testerServer+'/api/add_tester',
            data: JSON.stringify(testerGroup),
            dataType : 'text',
            async : false,
            success : function(data) {
                alert("success")
            },
            error : function() {
                alert("Error")
            }
        });
    }
}

function formatFormData(liObj){
	//form表单数据
	var span_list = liObj.children("span");
	var dataInfo = new Object();
	for(var m=1; m<(span_list.length-1); m++){
		var spanText = $(span_list[m]).text().split(":");
		dataInfo[spanText[0]] = spanText[1];
	}
	dataInfo["value"] = span_list.children("[name=tester_value]")[0].value;

	var formData = new back_env.TesterFormData();
	for(var key in dataInfo){
		if(key == "name" || key == "id" || key == "class"){
			formData["formType"] = back_env.EL_TYPE[key];
			formData["formElName"] = dataInfo[key];
			formData["index"] = dataInfo["index"];
		}else{
			if(key == "value"){
				formData["formElValue"] = dataInfo[key];
			}
		}
	}

	return formData;
}

function formatActionData(liObj){
	//action动作数据
	var span_list = liObj.children("span");
	var dataInfo = new Object();
	for(var m=1; m<span_list.length-1; m++){
		var spanText = $(span_list[m]).text().split(":");
		dataInfo[spanText[0]] = spanText[1];
	}

	if ($(span_list[span_list.length-1]).css('display') == "block"){
		dataInfo["value"] = span_list.children("[name=tester_result]")[0].value;
	}

	var actionData = new back_env.TesterActionData();
	for(var key in dataInfo){
		if(key == "name" || key == "id" || key == "class"){
			actionData["elType"] = back_env.EL_TYPE[key];
			actionData["elValue"] = dataInfo[key];
			actionData["index"] = dataInfo["index"];
		}else if(key == "value"){
			actionData["testerResult"] = dataInfo[key];
		}
	}
	actionData["action"] = back_env.ACTION_TYPE["click"];

	console.log(actionData);
	return actionData;
}

function formatTesterData(){
	var pathArray = getDomainAndPath($("[name=start_url]").val());

	var check_boxs = $(".tester_check");
	var actionNum = 0, formNum = 0;
	var testerListObj = new Array();
	var testerAction = new back_env.TesterAction();
	testerAction.urlPath = pathArray[1];

	var testerForms = new back_env.TesterForms("Tester", new Array());
	testerAction.forms.push(testerForms);
	for(var i=0; i<check_boxs.length; i++){
		var checkObj = $(check_boxs[i]);
		if(checkObj.prop("checked")==true){
			var liObj = checkObj.parent();
			var testerType = liObj.children("[name=tester_type]")[0];

			if($(testerType).text() == "form"){
				if(actionNum != formNum){
					testerListObj.push(testerAction);
					testerAction = new back_env.TesterAction();
					testerAction.urlPath = pathArray[1];

					testerForms = new back_env.TesterForms("Tester", new Array());
					testerAction.forms.push(testerForms);
					formNum = actionNum;
				}

				testerForms.params.push(formatFormData(liObj));
			}else{
				testerAction.actionList.push(formatActionData(liObj));

				actionNum++;
			}
		}
	}

	if(actionNum != formNum){
		testerListObj.push(testerAction);
	}

	return new back_env.TesterData(pathArray[0], testerListObj);
}

function getDomainAndPath(urlPath){
	var reg = new RegExp('^(https?|ftp|file)://[-a-zA-Z0-9+&@#%?=~_|!:,.;]*[/]', 'gm');

    var oldDomainP = urlPath.match(reg)[0];
	var domain = oldDomainP.substring(0, oldDomainP.length-1);
	var path = urlPath.substring(domain.length , urlPath.length);

	return new Array(domain , path);
}

// 添加选择确定的逻辑作为数据的校验信息准则
function setTesterInfo() {
	$("#tester_event_show").empty();// 先清空页面

	var tester_list = JSON.parse(localStorage.tester_list);

	for(var i=0; i<tester_list.length; i++){
		$("<div><span style='font-size:14px;font-weight:bold;margin-right:10px;'>URL:</span><input type='radio' name='start_url' value='"
			+tester_list[i].url+"' /><span style='color:red'>&nbsp;"+tester_list[i].url+"</span></div><hr>").appendTo($("#tester_event_show"))
		var ul = $("<ul class='sort_ul_deal'></ul>");
		for(var n=0; n<tester_list[i].events.length; n++){
			var li = initTesterEl(tester_list[i].events[n].tagName , tester_list[i].events[n].params);

			li.appendTo(ul);
		}
		ul.appendTo($("#tester_event_show"));

		$('.sort_ul_deal').sortable().bind('sortupdate', function() {});
	}

	$("input[name=start_url]:eq(0)").attr("checked",'checked'); 
}

function initTesterEl(tagName , elParam){
	var li;
	if(tagName == "SELECT"){
		li = setFormElement(tagName , elParam);
	}else if(tagName == "TEXTAREA"){
		li = setFormElement(tagName , elParam);
	}else if(tagName == "INPUT"){
		if(elParam["type"] == "text" || elParam["type"] == "password" || elParam["type"] == "tel"){
			li = setFormElement(tagName , elParam);
		}else if(elParam["type"] == "radio"){
			li = setFormElement(tagName , elParam);
		}else if(elParam["type"] == "checkbox"){
			li = setFormElement(tagName , elParam);
		}else{
			li = setActionElement(tagName , elParam);
		}
	}else{
		li = setActionElement(tagName , elParam);
	}

	return li;
}

/**
 * 作为form表单数据填写操作处理
 */
function setFormElement(tagName, elParam){
	var li = $("<li><input class='tester_check' style='margin-right:10px;' type='checkbox'/><span name='tester_type' style='margin-right:10px'>form</span>"
			  +"<span style='margin-right:20px;'>El:"+tagName+"</span></li>");

	if(tagName == "INPUT"){
		$("<span style='margin-right:20px;'>type:"+elParam["type"]+"</span>").appendTo(li);
	}

	if(elParam["id"] != "undefined" && elParam["id"] != null){
		$("<span style='margin-right:20px;'>id:"+elParam["id"]+"</span>").appendTo(li);
		if(elParam["id_index"] != "undefined" && elParam["id_index"] != null){
			$("<span style='margin-right:20px;'>index:"+elParam["id_index"]+"</span><br>").appendTo(li);
		}
	}else if(elParam["class"] != "undefined" && elParam["class"] != null){
		var cls_list = elParam["class"].split(" ");
		$("<span style='margin-right:20px;'>class:."+cls_list[cls_list.length-1]+"</span>").appendTo(li);
		if(elParam["class_index"] != "undefined" && elParam["class_index"] != null){
			$("<span style='margin-right:20px;'>index:"+elParam["class_index"]+"</span><br>").appendTo(li);
		}
	}else if(elParam["name"] != "undefined" && elParam["name"] != null){
		$("<span style='margin-right:20px;'>name:"+elParam["name"]+"</span>").appendTo(li);
		if(elParam["name_index"] != "undefined" && elParam["name_index"] != null){
			$("<span style='margin-right:20px;'>index:"+elParam["name_index"]+"</span><br>").appendTo(li);
		}
	}

	$("<br><span style='margin-right:20px;'>value:<input name='tester_value' type='text' style='margin-left:20px;' value='"+elParam["value"]+"'></input></span>").appendTo(li);

	return li;
}

/**
 * Action的对象元素自需要对应的id|name|class作为定位
 */
function setActionElement(tagName, elParam){
	var li = $("<li><input class='tester_check' style='margin-right:10px;' type='checkbox'/>"
			  +"<span name='tester_type' style='margin-right:10px'>action</span><span style='margin-right:20px;'>El:"+tagName+"</span></li>");

	if(elParam["id"] != "undefined" && elParam["id"] != null){
		$("<span style='margin-right:20px;'>id:"+elParam["id"]+"</span>").appendTo(li);
		if(elParam["id_index"] != "undefined" && elParam["id_index"] != null){
			$("<span style='margin-right:20px;'>index:"+elParam["id_index"]+"</span><br>").appendTo(li);
		}
	}else if(elParam["class"] != "undefined" && elParam["class"] != null){
		var cls_list = elParam["class"].split(" ");
		$("<span style='margin-right:20px;'>class:."+cls_list[cls_list.length-1]+"</span>").appendTo(li);
		if(elParam["class_index"] != "undefined" && elParam["class_index"] != null){
			$("<span style='margin-right:20px;'>index:"+elParam["class_index"]+"</span><br>").appendTo(li);
		}
	}else if(elParam["name"] != "undefined" && elParam["name"] != null){
		$("<span style='margin-right:20px;'>name:"+elParam["name"]+"</span>").appendTo(li);
		if(elParam["name_index"] != "undefined" && elParam["name_index"] != null){
			$("<span style='margin-right:20px;'>index:"+elParam["name_index"]+"</span><br>").appendTo(li);
		}
	}

	var tester_res = $("<span style='margin-right:20px;display:none;'>result:<input name='tester_result' type='text' style='margin-left:20px;'/></span>");
	tester_res.appendTo(li);

	li.dblclick(function(){
		if(tester_res.css('display') == "none"){
			tester_res.css('display','block');
		}else{
			tester_res.css('display','none');
		}
	});

	return li;
}

function setTesterLog(){
	$("#app_log_list").empty();

	var log_list = JSON.parse(localStorage.log_result);
	for(var i=0; i<log_list.length; i++){
		$("<li>"+log_list[i].message+"</li>").appendTo("#app_log_list");
	}
}

//设置测试引擎的类型
function setInitValue(){
	$("#testerServer").attr("value", localStorage.testerServer);

	$("#logLevel").text(localStorage.logLevel);

	if(back_env.testEngine != null){
		$("#engine_status").css("color", "green");
		$("#engine_status").text("Continue");
	}else{
		$("#engine_status").css("color", "red");
		$("#engine_status").text("Close");
	}

	var tester_engine = $("#testerEngine")
	if(localStorage.chrome != null){
		$("<option value='"+localStorage.chrome+"'>chrome</option>").appendTo(tester_engine);
	}else if(localStorage.firefox != null){
		$("<option value='"+localStorage.firefox+"'>firefox</option>").appendTo(tester_engine);
	}else if(localStorage.remote != null){
		$("<option value='"+localStorage.remote+"'>remote</option>").appendTo(tester_engine);
	}else if(localStorage.phantomjs != null){
		$("<option value='"+localStorage.phantomjs+"'>phantomjs</option>").appendTo(tester_engine);
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



/********************* 远程Tester服务数据 **********************/
function setSearchQueue(){
    $.get(localStorage.testerServer+"/api/search_queue", function(result){
        var queueObjList = JSON.parse(result);

        var queueOptions = $("#testQueue");
        for (var key in queueObjList){
            $("<option value='"+queueObjList[key]["id"]+"'>"+queueObjList[key]["queueName"]+"</option>").appendTo(queueOptions);
        }
    });
}