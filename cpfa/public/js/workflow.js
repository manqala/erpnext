
frappe.provide('cpfa');

frappe.ui.form.on('Workflow', {
	'refresh': function(frm){
		cpfa.set_docfields();
	},
	'document_type': function(frm){
		cpfa.set_docfields();
	},
})

frappe.ui.form.on('Workflow Transition', 'allowed', function(doc, cdt, cdn){
	frappe.model.set_value(cdt, cdn, 'allowed_user', '');
	cur_frm.refresh_field('transitions');
})

cpfa.getters = {
	get allowed() {
		if (cur_frm.cur_grid) {
			return cur_frm.cur_grid.doc.allowed || '000';
		}
		return '';
	}
}

cur_frm.set_query("allowed_user", "transitions", function() {
	return{
		filters: [["Has Role","role","=", cpfa.getters.allowed]],
		query: "cpfa.utils.queries.user_query"
	}
});

cpfa.set_docfields = function(){
	frappe.call({
		method: 'cpfa.utils.queries.get_docfields',
		args: {'doctype': cur_frm.doc.document_type},
		callback: function(r){
			if (r.message){
				cur_frm.get_field('transitions').grid
				.get_docfield('allowed_user_field').options = r.message;
				cur_frm.refresh_field('transitions');
			}
		}
	})
}