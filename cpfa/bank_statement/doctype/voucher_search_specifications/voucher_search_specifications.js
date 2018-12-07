// Copyright (c) 2018, Manqala and contributors
// For license information, please see license.txt


frappe.provide('cpfa');

frappe.ui.form.on('Voucher Search Specifications', {
	refresh: function(frm) {

	}
});

cpfa.getters = {
	get voucher_type() {
		if (cur_frm.cur_grid) {
			return cur_frm.cur_grid.doc.voucher_type || '000';
		}
		return '';
	}
}

cur_frm.set_query('voucher_type', "voucher_search_keys", function() {
	return{
		query: "cpfa.utils.queries.voucher_type_query"
	}
});

for (var i = 1; i <= 10; i++){
	let field = `field_${i}`;
	cur_frm.set_query(field, "voucher_search_keys", function() {
		return{
			filters: [{parent: ['=', cpfa.getters.voucher_type]},
					  {hidden: ['=', 0]},
					  {fieldtype: ['not in', ['Column Break','Section Break','Table']]}],
			query: "cpfa.utils.queries.docfield_query"
		}
	});
	
	frappe.ui.form.on('Voucher Search Key', field, function(frm, dt, dn){
		var doc = locals[dt][dn];
		var val = doc[field];
		if ((doc.search_key_specification || '').indexOf(val) !== -1){
			frappe.model.set_value(dt, dn, field, '');
			return;
		}
		
		frappe.call({
			method: 'transform_fields',
			args: {dn: dn},
			doc: cur_frm.doc,
			callback: function(r){
				var txt = r ? (r.message || '') : '';
				frappe.model.set_value(dt, dn, "search_key_specification", txt);
			}
		})
	})

	frappe.ui.form.on('Voucher Search Key', `field_${i}_transformation_rule`,
		function(frm, dt, dn){
			var old_sks = locals[dt][dn]['search_key_specification'] || '';
			var old_val = locals[dt][dn][field] || '';
			frappe.call({
				method: 'transform_field',
				args: {'field': field, 'dn':dn},
				doc: frm.doc,
				callback: function(r){
					var txt = r ? (r.message || '') : '';
					var sks = old_sks.replace(old_val, txt)
					frappe.model.set_value(dt, dn, "search_key_specification", sks);
				}
			})
		}
	);
}

frappe.ui.form.on('Voucher Search Key', 'separator', function(frm, dt, dn){
	var doc = locals[dt][dn];
	if (!doc.search_key_specification) return;
	
	frappe.call({
		method: 'transform_fields',
		args: {dn: dn},
		doc: cur_frm.doc,
		callback: function(r){
			var txt = r ? (r.message || '') : '';
			frappe.model.set_value(dt, dn, "search_key_specification", txt);
		}
	})
})

















frappe.ui.form.ControlLink.prototype.validate_link_and_fetch = function(df, doctype, docname, value) {
	var me = this;

	if(value) {
		return new Promise((resolve) => {
			var fetch = '';

			if(this.frm && this.frm.fetch_dict[df.fieldname]) {
				fetch = this.frm.fetch_dict[df.fieldname].columns.join(', ');
			}
			var method = df.options == 'DocField' ? 
							'cpfa.utils.validate_link' :
							'frappe.desk.form.utils.validate_link'
			return frappe.call({
				method: method,
				type: "GET",
				args: {
					'value': value,
					'options': doctype,
					'fetch': fetch
				},
				no_spinner: true,
				callback: function(r) {
					if(r.message=='Ok') {
						if(r.fetch_values && docname) {
							me.set_fetch_values(df, docname, r.fetch_values);
						}
						resolve(r.valid_value);
					} else {
						resolve("");
					}
				}
			});
		});
	}
}
