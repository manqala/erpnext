// Copyright (c) 2018, frappe and contributors
// For license information, please see license.txt

frappe.ui.form.on('Vehicle Request', {
	refresh: function(frm) {
		frappe.call({
			args:{},
			method:"cpfa.fleet.doctype.vehicle_request.vehicle_request.getEmployeeName",
			callback:function(r){
			cur_frm.set_df_property("employee_name","options",r.message)
			cur_frm.refresh_field("employee_name")
			//console.log(r.message)
			}
		})
	},
	employee_name:function(frm){
		frappe.call({
			method:"frappe.client.get_value",
			args:{
				doctype:"Employee",
				filters:{employee_name:cur_frm.doc.employee_name},
				fieldname:['user_id',"name"],
			},
			callback: function(r){
				console.log(r.message);
				cur_frm.set_value("employee_email",r.message.user_id)
				cur_frm.set_value("employee",r.message.name)
			}

		})
	}

});
