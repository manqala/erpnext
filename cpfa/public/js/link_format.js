frappe.form.link_formatters['Vehicle Location'] = function(value, doc) {
	if(doc && doc.vehicle_location && doc.vehicle_location !== value) {
		return value? value + ': ' + doc.vehicle_location: doc.vehicle_location;
	} else {
		return value;
	}
}
