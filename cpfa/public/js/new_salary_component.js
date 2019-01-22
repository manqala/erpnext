frappe.ui.form.on("Salary Slip",{
  employee:function(frm){
    if(frm.doc.salary_slip_based_on_timesheet){
      var duration=frm.doc.total_working_hours
      var employee=frm.doc.employee
      var structure=frm.doc.salary_structure
      var rate= frm.doc.hour_rate
      var start_date=frm.doc.start_date
      var end_date=frm.doc.end_date
      var twd=frm.doc.total_working_days
      var cur_form=frm.doc.earnings

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
      cur_frm.doc.earnings.length=0
      cur_frm.doc.earnings=[]
      cur_frm.doc.earnings==r.message
      cur_frm.refresh_field("earnings")
      // for(var i=0;i<r.message.length;i++){
      //   for(var j=0;j<frm.doc.earnings.length;j++){
      //   if(r.message[i].salary_component==cur_frm.doc.earnings[j].salary_component){
      //     var val=r.message[i].accrual_basis
      //     frm.doc.earnings[j].accrual_basis=val
      //   console.log(val);
      //   }
      //   }
      // }
      // for(var k=0;k<frm.doc.earnings.length;k++){
      //   console.log(frm.doc.earnings[k].accrual_basis);
      // }
      // cur_frm.refresh_field("earnings")
      }
    })

    }
},
})
