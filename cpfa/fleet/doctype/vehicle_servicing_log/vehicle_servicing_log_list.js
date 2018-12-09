// frappe.listview_settings['Vehicle Servicing Log'] = {
//     	add_fields: ["service_status"],
//     	get_indicator: function(doc) {
//     		var colors{
//           "Service In Progress": "green",
//           "Returned": "orange"
//         }
//         return[__(doc.service_status),colors[doc.service_status],"Service Status,=," + doc.service_status]
//     	}
//     };

frappe.listview_settings['Vehicle Servicing Log'] = {
	add_fields: ["service_status"],
	get_indicator: function (doc) {
		return [__(doc.service_status), {
			"Service In Progress": "blue",
			"Returned": "green",
		}[doc.service_status], "service_status,=," + doc.service_status];
	}
};
