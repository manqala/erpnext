// Copyright (c) 2019, Manqala and contributors
// For license information, please see license.txt

frappe.ui.form.on('Overtime Application', {
	//  disp:function(frm) {
	// 	status=false;
	// 	return status= true ? false: true
	// },
		validate:function(frm){
			var date_ =frm.doc.date
			frappe.call({
				method:"cpfa.cpfa.doctype.overtime_application.overtime_application.date_append",
				args:{
					date:date_
				},
				callback:function(r){
					console.log(r.message);
				}
			})
		},
	 refresh: function(frm) {
 		if(frm.doc.__islocal){
	 	;
 	}
	 	else{
			var status=false;
	 		frm.add_custom_button(("Confirm Overtime"),function(ev){
				emp=frm.doc.employee
				frappe.call({
					args:{emp:emp},
					method:"cpfa.utils.misc_methods.get_val",
					callback:function(r){
						var id=r.message
						if(id==frappe.user.name){
							if(status==true){
							 frm.toggle_display("actual_period_spent_on_job",false)
							 status=false
							 frm.set_value("status","Approved");
							 frm.refresh_field("status")
						 }
						else if(status==false){
							 frm.toggle_display("actual_period_spent_on_job",true)
							 status=true
							 frm.set_df_property("actual_period_spent_on_job","read_only",0);
							 frm.set_value("status","Confirmed");
							 cur_frm.refresh_fields()
						 }
						}
					 else{

						 frappe.throw("Only Owner of Overtime Application Can Confirm!")
					 }
					}
				})

				}
			)
			;
	 	}
	 },
	date: function(frm){
		var today = new Date();
   	var dd = today.getDate();
   	var mm = today.getMonth()+1; //January is 0!
   	var yyyy = today.getFullYear();
   	if(dd<10) {
   	    dd = '0'+dd
   	}
   	if(mm<10) {
   	    mm = '0'+mm
   	}
   	today = yyyy + '-' + mm + '-' + dd;
		if(today>frm.doc.date){
			frm.doc.date="";
			frm.refresh_field("date")
			frappe.throw("Selected date cannot be in the past")
		}
		else{
			;
		}

	}
});
