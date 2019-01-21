frappe.ui.form.on("Salary Slip",{
  employee:function(frm){
    var duration=frm.doc.total_working_hours
    var employee=frm.doc.employee
    var structure=frm.doc.salary_structure
    var rate= frm.doc.hour_rate
    var start_date=frm.doc.start_date
    var end_date=frm.doc.end_date
    var twd=frm.doc.total_working_days
    var cur_form=frm.doc
  frappe.call({
    method:
      "cpfa.utils.salary_slip_methods.comp_calc",
  args:{
     duration:duration,
     employee:employee,
     structure:structure,
     rate:rate,
     start_date:start_date,
     end_date:end_date,
     twd:twd,
     cur_form:cur_form
   },
    callback:function(r){
    //frm.refresh_fields["earnings","deductions"]
    console.log(r.message);
    }
  })
},
})
