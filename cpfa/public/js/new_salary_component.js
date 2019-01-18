frappe.ui.form.on("Salary Slip",{
  employee:function(frm){
    var duration=frm.doc.total_working_hours
    var employee=frm.doc.employee
    var structure=frm.doc.salary_structure
    var rate= frm.doc.hour_rate
  frappe.call({
    method:
      "cpfa.utils.salary_slip_methods.comp_based_on_timesheet",
  args:{
     duration:duration,
     employee:employee,
     structure:structure,
     rate:rate,
   },
    callback:function(r){
      console.log(r.message);
    }
  })
},
})
