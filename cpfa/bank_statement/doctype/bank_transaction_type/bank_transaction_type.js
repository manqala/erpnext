// Copyright (c) 2017, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

cur_frm.set_query("credit_account", function(doc) {
	return {
		filters: {
			'root_type': 'Liability',
			'is_group': 0
		}
	}
});

cur_frm.set_query("debit_account", function(frm) {
	return {
		filters: {
			'root_type': 'Asset',
			'is_group': 0
		}
	}
});

cur_frm.set_query("gl_posting_credit_account", function(frm) {
	return {
		filters: {
			'root_type': 'Liability',
			'is_group': 0
		}
	}
});

cur_frm.set_query("gl_posting_debit_account", function(frm) {
	return {
		filters: {
			'root_type': 'Asset',
			'is_group': 0,
		}
	}
});


frappe.ui.form.on('Bank Transaction Type', {
	refresh: function(frm) {

	}
});


frappe.ui.form.on('Transaction Type Journal Template', 'party_type',
	function(frm, dt, dn){
		var doc = locals[dt][dn];
		frappe.model.set_value(dt, dn, "party_type_doctype", doc.party_type);
	}
);