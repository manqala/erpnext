	frappe.form.link_formatters['Vehicle Location'] = function(value, doc) {
		if(doc && doc.location_name && doc.location_name !== value) {
			return value? value + ':'+ doc.location_name: doc.location_name;
		} else {
			return value;
		}
	}

	frappe.form.link_formatters['Vehicle Trip Log'] = function(value, doc) {
		if(doc && doc.employee_name && doc.employee_name !== value) {
			return value? value + ': ' + doc.employee_name: doc.employee_name;
		} else {
			return value;
		}
	}
