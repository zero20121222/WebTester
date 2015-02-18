jQuery("<div id='tester_wait_body_view' class='tester_wait_body_view'>Wait ready web by WebTester!</div>").prependTo(jQuery(document.body));
jQuery(document).ready(function($) {
	$("#tester_wait_body_view").text("Ready Web Ok!");

	setTimeout(function(){
		$("#tester_wait_body_view").hide();
	}, 1000);

	$("<div class='tester_theme_auto_window' id='tester_show_element_view'><div class='tester_theme_poptit'><a href='javascript:;' id='tester_show_close' title='关闭' class='close'>×</a><h3>Element Detail<span id='tester_element_tagName' style='color:red;margin-left:20px;'></span></h3></div><div class='tester_dform' style='text-align:left'><form class='tester_contact_form' name='queue_form' method='post'></form></div></div><div class='tester_theme_popover_mask'></div>").appendTo($(document.body));

    $('#tester_show_close').click(function(){
        $('.tester_theme_popover_mask').fadeOut(100);
        $('#tester_show_element_view').slideUp(200);
    })
	$(document).mousedown(function(e){ 
		//show detail element info in window
		if(e.altKey && 1 == e.which){
			//right click
			obj = $(e.target);

			$("#tester_element_tagName").text(obj[0].tagName);
			$(".tester_contact_form").empty();

			$(create_view(obj)).appendTo($(".tester_contact_form"));

			$('.tester_theme_popover_mask').fadeIn(100);
            $('#tester_show_element_view').slideDown(200);
		}

		//save element event for click
		if(e.metaKey && 1 == e.which){
			obj = $(e.target);
			create_view(obj);
		}
	});
});

function create_view(event_obj){
	var ul = $("<ul></ul>"); 

	switch(event_obj[0].tagName){
		case "A":
			form_obj = __init_back_obj(create_a_view(ul, event_obj));
			break;
		case "BUTTON":
			form_obj = __init_back_obj(create_button_view(ul, event_obj));
			break;
		case "FORM":
			form_obj = __init_back_obj(create_form_view(ul, event_obj));
			break;
		case "IMG":
			form_obj = __init_back_obj(create_img_view(ul, event_obj));
			break;
		case "INPUT":
			form_obj = __init_back_obj(create_input_view(ul, event_obj));
			break;
		case "LINK":
			form_obj = __init_back_obj(create_link_view(ul, event_obj));
			break;
		case "SELECT":
			form_obj = __init_back_obj(create_select_view(ul, event_obj));
			break;
		default:
			form_obj = __init_back_obj(basic_view(ul, event_obj));
	}

	if(!__exist_obj_lock(form_obj)){
		return create_view($(event_obj).parent());
	}else{
		__save_form(event_obj[0].tagName , form_obj);
		return ul;
	}
}

function basic_view(ul, event_obj){
	return __set_li_back_obj(ul, ["id", "class", "style", "title"], event_obj);
}


function create_a_view(ul, event_obj){
	// <a> href、 target、 ping、 rel、 media、 hreflang、 type
	var back_obj = basic_view(ul, event_obj);
	return back_obj.concat(__set_li_back_obj(ul, ["href", "target", "type"], event_obj));
}

function create_button_view(ul, event_obj){
	// <button>        autofocus、 disabled、 form、 formaction、 formenctype、 formmethod、 formnovalidate、 formtarget、 name、 type、 value
	var back_obj = basic_view(ul, event_obj);
	return back_obj.concat(__set_li_back_obj(ul, ["name", "type", "value"], event_obj));
}

function create_form_view(ul, event_obj){
	// <form>          accept-charset、 action、 autocomplete、 enctype、 method、 name、 novalidate、 target
	var back_obj = basic_view(ul, event_obj);
	return back_obj.concat(__set_li_back_obj(ul, ["name", "target", "action", "method"], event_obj));
}

function create_img_view(ul, event_obj){
	// <img>           alt、 src、 usemap、 ismap、 width、 height
	var back_obj = basic_view(ul, event_obj);
	return back_obj.concat(__set_li_back_obj(ul, ["src", "width", "height"], event_obj));
}

function create_input_view(ul, event_obj){
	// <input>   checked、 dirname、 disabled、 form、 formaction、 formenctype、 formmethod、 formnovalidate、 formtarget、 height、 list、 max、 maxlength、 min、 multiple、 name、 pattern、 placeholder、 readonly、 required、 size、 src、 step、 type、 value、 width
	var back_obj = basic_view(ul, event_obj);
	return back_obj.concat(__set_li_back_obj(ul, ["name", "src", "type", "value", "checked"], event_obj));
}

function create_link_view(ul, event_obj){
	// <link>          href、 rel、 media、 hreflang、 type、 sizes
	var back_obj = basic_view(ul, event_obj);
	return back_obj.concat(__set_li_back_obj(ul, ["href", "rel", "type"], event_obj));
}

function create_select_view(ul, event_obj){
	// <select>        autofocus、 disabled、 form、 multiple、 name、 required、 size
	var back_obj = basic_view(ul, event_obj);
	return back_obj.concat(__set_li_back_obj(ul, ["name", "value"], event_obj));
}

function ElementObj(attrName, attrValue){
	this.attrName = attrName;
	this.attrValue = attrValue;
}

function __li_view(attr_v, event_obj){
	var view_val = new Array();
	var li_view = "<li><span>"+attr_v+":</span>";
	if(attr_v == "value"){
		if(event_obj.val() == "undefined" || event_obj.val() == null){
			li_view += "<span>"+event_obj.val()+"</span></li>";
			view_val.push(li_view);
		}else{
			li_view += "<span style='color:red'>"+event_obj.val()+"</span></li>";
			view_val.push(li_view);
			if(attr_v != "style"){
				view_val.push(JSON.parse("{\""+attr_v+"\":\""+event_obj.val()+"\"}"));
			}
		}
	}else{
		if(event_obj.attr(attr_v) == "undefined" || event_obj.attr(attr_v) == null){
			li_view += "<span>"+event_obj.attr(attr_v)+"</span></li>";
			view_val.push(li_view);
		}else{
			li_view += "<span style='color:red'>"+event_obj.attr(attr_v)+"</span></li>";
			view_val.push(li_view);
			if(attr_v != "style"){
				view_val.push(JSON.parse("{\""+attr_v+"\":\""+event_obj.attr(attr_v)+"\"}"));
			}
		}
	}

	return view_val;
}

function __li_list_view(attr_s, event_obj){
	var obj_list = new Array();
	for(var i=0; i<attr_s.length; i++){
		obj_list.push(__li_view(attr_s[i], event_obj))
	}
	return obj_list;
}

function __set_li_back_obj(ul, attr_s, event_obj){
	var obj_list = __li_list_view(attr_s, event_obj);

	var back_obj = new Array();
	for(var i=0; i<obj_list.length; i++){
		$(obj_list[i][0]).appendTo(ul);
		if(obj_list[i].length > 1){
			back_obj.push(obj_list[i][1]);
		}
	}

	return back_obj;
}

function __init_back_obj(back_obj){
	var obj = new Object();
	for(var n=0; n<back_obj.length; n++){
		for(key in back_obj[n]){
			obj[key] = back_obj[n][key];
		}
	}

	return obj;
}

function __save_action(){
	var send_obj = {
		test_type:"form",
		params:{
			el_name:"INPUT",
			el_type:"text"
		}
	};
	chrome.extension.sendRequest({data:send_obj}, function(data) {});
}

function __exist_obj_lock(obj){
	if(obj["name"] != "undefined" && obj["name"] != null){
		return true;
	}else if(obj["id"] != "undefined" && obj["id"] != null){
		return true;
	}else if(obj["class"] != "undefined" && obj["class"] != null){
		return true;
	}

	return false;
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
function __save_form(tag_name, form_obj){
	var send_obj = {
		test_type:"form",
		tagName:tag_name,
		params:form_obj
	};
	chrome.extension.sendRequest({data:send_obj}, function(data) {});
}