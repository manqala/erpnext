frappe.ui.form.on("Salary Slip",{
  employee:function(frm){
    if(frm.doc.salary_slip_based_on_timesheet){
      var cur_form=JSON.stringify(frm.doc)

    frappe.call({
      method:
        "cpfa.utils.salary_slip_methods.comp_calc",
    args:{
       cur_form:cur_form
     },
      callback:function(r){
      // console.log(r.message);
      setTimeout(function(){
        frappe.model.sync(r.docs);
        cur_frm.refresh_fields()
      },1000);
      // cur_frm.doc.earnings.length=0
      // cur_frm.doc.earnings=[]
      // cur_frm.doc.earning=0
      // cur_frm.doc.earnings==r.message
      // cur_frm.refresh_field("earnings")
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
