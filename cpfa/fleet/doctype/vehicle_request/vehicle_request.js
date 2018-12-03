// Copyright (c) 2018, frappe and contributors
// For license information, please see license.txt

 frappe.ui.form.on('Vehicle Request', {
// 	refresh: function(frm) {
// 		frappe.call({
// 			args:{},
// 			method:"cpfa.fleet.doctype.vehicle_request.vehicle_request.getEmployeeName",
// 			callback:function(r){
// 			cur_frm.set_df_property("employee_name","options",r.message)
// 			cur_frm.refresh_field("employee_name")
// 			//console.log(r.message)
// 			}
// 		})
// 	},
	// employee_name:function(frm){
	// 	frappe.call({
	// 		method:"frappe.client.get_value",
	// 		args:{
	// 			doctype:"Employee",
	// 			filters:{employee_name:cur_frm.doc.employee_name},
	// 			fieldname:['user_id',"name","prefered_email"],
	// 		},
	// 		callback: function(r){
	// 			console.log(r.message);
	//
	// 			if(r.message.user_id==null){
	// 				cur_frm.set_value("employee_email",r.message.prefered_email)
	// 			}
	// 			else{
	// 				cur_frm.set_value("employee_email",r.message.user_id)
	// 			}
	// 			cur_frm.set_value("employee",r.message.name)
	// 		}
	//
	// 	})
	// }
date_required:function(frm) {
	var today = new Date();
	var dd = today.getDate();
	var mm = today.getMonth()+1; //January is 0!
	var yyyy = today.getFullYear();
	if(dd<10) {
	    dd = '0'+dd
	}
	if(mm<10) {
	    mm = '0'+mm
	}
	today = yyyy + '-' + mm + '-' + dd;
	var docdate=cur_frm.doc.date_required
	if(docdate<today){
	  cur_frm.doc.date_required=""
	  cur_frm.refresh_field("date_required")
	  frappe.throw("Selected date cannot be in the past.")
	}
	else{
	}
},
vehicle_type_required:function(frm){
	cur_frm.fields_dict["vehicle_assigned"].get_query=function(doc){
		return {
			filters:{
				"vehicle_type":frm.doc.vehicle_type_required,
				//console.log("Finished")
		}
	}
	}
}
// time_required:function(frm){
// 	var today = new Date();
// 	var dd = today.getDate();
// 	var mm = today.getMonth()+1; //January is 0!
// 	var yyyy = today.getFullYear();
// 	if(dd<10) {
// 	    dd = '0'+dd
// 	}
// 	if(mm<10) {
// 	    mm = '0'+mm
// 	}
// 	today = yyyy + '-' + mm + '-' + dd;
// 	time_now=new Date().getHours()+":"+new Date().getMinutes()+":"+new Date().getSeconds()
// 	console.log(time_now);
// 	console.log(cur_frm.doc.time_required);
// }
});
