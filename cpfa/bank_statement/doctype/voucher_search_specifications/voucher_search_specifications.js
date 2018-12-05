// Copyright (c) 2018, Manqala and contributors
// For license information, please see license.txt


frappe.ui.form.on('Voucher Search Specifications', {
	refresh: function(frm) {
		for (var i = 1; i <= 10; i++){
			let field = `field_${i}`;
			frm.set_df_property(field, 'ignore_link_validation', true, frm.doc.name, 'voucher_search_keys')
			frm.set_query(field, "voucher_search_keys", function() {
				return{
					filters: [{parent: ['=', 'Sales Invoice']}],
					query: "cpfa.utils.queries.docfield_query"
				}
			});
		}
		frm.refresh_field('voucher_search_keys');
	},
	voucher_search_keys: function(frm) {
	}
});

frappe.ui.form.on('Voucher Search Key', 'voucher_type',
	function(frm, dt, dn) {
	}
);
