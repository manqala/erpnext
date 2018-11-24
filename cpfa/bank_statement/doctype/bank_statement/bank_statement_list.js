// Copyright (c) 2017, Manqala Ltd. and contributors
// For license information, please see license.txt


frappe.listview_settings['Bank Statement'] = {
	add_fields: ["status"],
	get_indicator: function(doc) {
		if(doc.status === 'Completed') {
			return [__("Completed"), "green", "status,=,Completed"]
		}else if(doc.status === 'Partially Completed'){
			return [__("Partially Completed"), "yellow", "status,=,Partially Completed"]
		}else if(doc.status === 'Not Started'){
			return [__("Not Started"), "darkgrey", "status,=,Not Started"]
		}
	}
	// right_column: "grand_total"
};
