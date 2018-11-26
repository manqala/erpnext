// Copyright (c) 2018, frappe and contributors
// For license information, please see license.txt

frappe.ui.form.on('Vehicle Request', {
	refresh: function(frm) {
		frappe.call({
			method:"frappe.client.get_value",
			args:{
				doctype:"Employee",
			//	filters:{employee_name:},
				fieldname:["employee_name"],
				callback:function(r){
					// frm.set_df_property('employee_name', 'options', r.message);
					// frm.refresh_field('employee_name');
					console.log(r.message);

				}
			},
		})

	}

});
