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
