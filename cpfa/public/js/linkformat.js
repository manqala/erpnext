	frappe.form.link_formatters['Vehicle Location'] = function(value, doc) {
		if(doc && doc.location_name && doc.location_name !== value) {
			return value? value + ':'+ doc.location_name: doc.location_name;
		} else {
			return value;
		}
	}
