// Copyright (c) 2018, Manqala and contributors
// For license information, please see license.txt


cur_frm.set_query('voucher_type', "voucher_search_keys", function() {
	return{
		query: "cpfa.utils.queries.voucher_type_query"
	}
});

frappe.ui.form.on('Voucher Search Specifications', {
	refresh: function(frm) {
		for (var i = 1; i <= 10; i++){
			let field = `field_${i}`;
			frm.set_df_property(field, 'ignore_link_validation', true, frm.doc.name, 'voucher_search_keys')

			for (var j=frm.doc.voucher_search_keys.length; j>0; j--){
				var voucher_type = frm.doc.voucher_search_keys[j].voucher_type;
				frm.set_query(field, "voucher_search_keys", function() {
					return{
						filters: [{parent: ['=', voucher_type]}],
						query: "cpfa.utils.queries.docfield_query"
					}
				});
			}
		}
		frm.refresh_field('voucher_search_keys');

	},
});

frappe.ui.form.on('Voucher Search Key', 'voucher_type',
	function(frm, dt, dn) {
		for (var i = 1; i <= 10; i++){
			let field = `field_${i}`;
			frm.set_df_property(field, 'ignore_link_validation', true, frm.doc.name, 'voucher_search_keys')
			
			for (var j=frm.doc.voucher_search_keys.length; j>0; j--){
				var voucher_type = locals[dt][dn]['voucher_type'];
				frm.set_query(field, "voucher_search_keys", function() {
					return{
						filters: [{parent: ['=', voucher_type]}],
						query: "cpfa.utils.queries.docfield_query"
					}
				});
			}
		}
		frm.refresh_field('voucher_search_keys');
	}
);

for (var i = 1; i <= 10; i++){
	let field = `field_${i}`;
	frappe.ui.form.on('Voucher Search Key', field, function(frm, dt, dn){
		var doc = locals[dt][dn];
		if (doc.search_key_specification){
			var val = doc.search_key_specification + doc.separator||'' + doc[field]
			frappe.model.set_value(dt, dn, "search_key_specification", val)
		} else if(doc[field]) {
			frappe.model.set_value(dt, dn, "search_key_specification", doc[field])
		}
	})
}