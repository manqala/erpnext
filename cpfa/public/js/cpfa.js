
$( document ).ready(function(){
	try {
		
		frappe.workflow.get_transitions = function(doctype, state){
			frappe.workflow.setup(doctype);
			return frappe.call({
				method: 'cpfa.utils.workflow.get_transitions',
				args: {doc: cur_frm.doc}
			})
		}

		frappe.ui.form.States.prototype.show_actions = function(state) {
			var added = false,
				me = this;

			this.frm.page.clear_actions_menu();

			// if the loaded doc is dirty, don't show workflow buttons
			if (this.frm.doc.__unsaved===1) {
				return;
			}

			function has_approval_access(transition) {
				let approval_access = false;
				const user = frappe.session.user;
				if (user === 'Administrator'
					|| transition.allow_self_approval
					|| user !== me.frm.doc.owner) {
					approval_access = true;
				}
				return approval_access;
			}

			frappe.workflow.get_transitions(this.frm.doctype, state).then(transitions=>{
				$.each(transitions.message, function(i, d){
					if(frappe.user_roles.includes(d.allowed) && has_approval_access(d)) {
						added = true;
						me.frm.page.add_action_item(__(d.action), function() {
							frappe.call({
								method: 'cpfa.utils.workflow.apply_workflow',
								args: {doc: me.frm.doc, action: d.action},
								callback: function(r){
									frappe.model.sync(r.message);
									me.frm.refresh();
								}
							});
						});
					}
				});
			});

			if(added) {
				this.frm.page.btn_primary.addClass("hide");
				this.frm.toolbar.current_status = "";
				this.setup_help();
			}
		};

	} catch(e){
		console.trace('cpfa.js error')
		console.trace(e)
	}
})
