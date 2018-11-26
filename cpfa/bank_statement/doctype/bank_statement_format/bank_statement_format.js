// Copyright (c) 2017, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Bank Statement Format', {
	refresh: function(frm) {
		frm.trigger('txn_type_derivation');
	},
	
	txn_type_derivation: (frm)=>{
		var txn_types = frappe.meta.get_docfield('Bank Statement Mapping Item', 'target_field').options
		txn_types = txn_types.split('\n')
		
		if(frm.doc.txn_type_derivation !== 'Map From Statement'){
			txn_types.splice(txn_types.indexOf('Transaction Type'),1)
			frm.set_df_property('target_field', 'options', txn_types, frm.doc.name, 'bank_statement_mapping_item')
		} else {
			frm.set_df_property('target_field', 'options', txn_types, frm.doc.name, 'bank_statement_mapping_item')
		}

		frm.refresh_field('bank_statement_mapping_item');
	}
});
