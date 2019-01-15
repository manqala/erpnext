// Copyright (c) 2017, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

var acc_currency_map = {},
	statement_date_overlap,
	account_types,
	render_indicators,
	statement_first_validate = true

frappe.ui.form.on('Bank Statement', {
	refresh: (frm)=>{
		render_indicators();
		frm.add_custom_button(__("Process Statement"), function() {
			frappe.call({
				method: 'process_statement',
				doc: frm.doc,
				freeze: true,
				callback: function(r){
					render_indicators();
					frm.refresh_field('bank_statement_items');
				}
			})
		});
		
		frm.add_custom_button(__("Upload Statement"), function() {
			frappe.call({
				method: 'fill_table',
				doc: frm.doc,
				freeze: true,
				callback: function(r){
					var set_margin = function(){
						$('.msgprint hr').attr('style', 'margin: 3px');
					}
					setTimeout(set_margin, 300);
					frm.refresh();
				}
			})
		});
		
		frm.add_custom_button("Delete Postings", function(){
			frappe.confirm('Delete Journal Entries?', function(){
				frappe.call({
					method: 'delete_postings',
					doc: frm.doc,
					freeze: true,
					callback: function(r){
						render_indicators();
						frm.refresh_field('bank_statement_items');
						frappe.msgprint('Journal Entries Deleted')
					}
				})
			});
		})
		
		var last_btn = frm.page.inner_toolbar[0];
		if (last_btn){
			last_btn.lastChild.classList.add('btn-danger');
		}
		
		if (frm.doc.bank){
			frm.trigger('bank');
		}
	},
	bank: (frm)=>{
		frappe.call({
			method: "get_account_no",
			doc: frm.doc,
			callback: function(d){
				if (d.message){	
					frm.set_df_property("account_no", "options", d.message.acc_nos);
					acc_currency_map.map = d.message.currency_map
					account_types = d.message.account_types
					frm.trigger('set_account_type_options');
				}
			}
		})
	},
	account_no: (frm)=>{
		if (acc_currency_map.map){
			frm.set_value('account_currency', acc_currency_map.map[frm.doc.account_no])
			frm.refresh_field('account_currency')
		}
	},
	statement_start_date: (frm)=>{
		frappe.call({
			method: "check_end_date",
			doc: frm.doc,
			callback: function(d){
				if (d.message){	
					statement_date_overlap = d.message.gap
				}
			}
		})
	},
	validate: (frm)=>{
		if ((statement_date_overlap) && (statement_first_validate)){
			frappe.confirm(
				"There is a gap in the previous statement's end date and the specified start date (" + statement_date_overlap + " days). <br><b>Continue</b>?",
				()=>{statement_first_validate=false;frm.save();},
				()=>show_alert('Document save cancelled')
			)
			frappe.validated = false
			return false
		}
	},
	set_account_type_options: function(doc, cdt, cdn) {
		var df1 = frappe.meta.get_docfield("Bank Statement Item","jl_debit_account_type", cur_frm.doc.name);
		df1.options = account_types
		var df2 = frappe.meta.get_docfield("Bank Statement Item","jl_credit_account_type", cur_frm.doc.name);
		df2.options = account_types
		cur_frm.refresh_field('bank_statement_items');
    }
});


//frappe.ui.form.on('Bank Statement Item', 'jl_debit_account_type', (frm, dt, dn)=>{
//	cur_frm.fields_dict["bank_statement_items"].grid.get_field("jl_debit_account").get_query = function(doc){
//	       return {
//	               "filters":{
//	                       "account_type": locals[dt][dn].jl_debit_account_type
//	               }
//	       }
//	}
//});

cur_frm.set_query("jl_debit_account", "bank_statement_items", function(doc, cdt, cdn) {
	var d = locals[cdt][cdn];
	return{
		filters: [
			['Account', 'account_type', '=', d.jl_debit_account_type],
		]
	}
});
cur_frm.refresh_field('bank_statement_items');

cur_frm.set_query("jl_credit_account", "bank_statement_items", function(doc, cdt, cdn) {
	var d = locals[cdt][cdn];
	return{
		filters: [
			['Account', 'account_type', '=', d.jl_credit_account_type],
		]
	}
});
cur_frm.refresh_field('bank_statement_items');


frappe.ui.form.on('Bank Statement Item', 'post_manually', (frm, dt, dn)=>{
	frappe.show_alert('Post manually')
	return false;
})

render_indicators = function(){
	if (!cur_frm.doc.bank_statement_items) return;

	var rows = cur_frm.fields_dict['bank_statement_items'].grid.grid_rows;
	$.each(rows, function(i,row){
		let col = row.columns.status.find('.static-area.ellipsis');
		col.removeClass('indicator orange green red');
		if (['Pending','To Clear'].indexOf(row.doc.status) != -1){
			col.addClass('indicator orange');
		} else if (row.doc.status == 'Completed'){
			col.addClass('indicator green');
		} else if (row.doc.status == 'Not Started'){
			col.addClass('indicator red');
		}
	})
}