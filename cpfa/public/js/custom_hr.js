
frappe.ui.form.on('Salary Slip', {
	refresh: function(frm){

	},
	toggle_fields: function(frm) {
		frm.toggle_display(['hourly_wages', 'timesheets'],
			cint(frm.doc.salary_slip_based_on_timesheet)==1);

		frm.toggle_display(['payment_days', 'total_working_days', 'leave_without_pay'],
			frm.doc.payroll_frequency!="");
	},
	employee: function(frm){
		var employee = frm.doc.employee_name
		if(employee==undefined){
			;
		}
		/*A function that calculates the daily salary of employee and  returns the amount payable after deductions*/
		else{
		frappe.call({
				args:{employee:frm.doc.employee},
				method: 'cpfa.utils.misc_methods.get_timesheet',
				callback: function(response){
					total_=0
					console.log(response.message);
					cur_frm.clear_table("timesheets")
 	 					for(var o=0;o<response.message.length;o++){
 	 						frm.add_child("timesheets")
							frm.doc.timesheets[o].time_sheet=response.message[o].name
							frm.doc.timesheets[o].working_hours=response.message[o].total_hours
							total_+=response.message[o].total_hours
 	 					//	frm.doc.timesheets[o].=response.message[o].name
 	 					}
						frm.doc.total_working_hours=total_
						console.log(total_);
						//frm.toggle_display("timesheets", true)
						frm.trigger("toggle_fields");
 	           	frm.refresh_field("timesheets")
			}
		})
	}
	}
})
