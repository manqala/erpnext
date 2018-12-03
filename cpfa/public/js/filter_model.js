frappe.ui.form.on('Vehicle',{
  vehicle_make: function(frm){
    //console.log("At the beginning")
      cur_frm.fields_dict["vehicle_model"].get_query=function(doc){
        return {
          filters:{
            "vehicle_make":frm.doc.vehicle_make,
            //console.log("Finished")
        }
      }
      }
  },
  refresh: function(frm){
    if(frm.doc.__islocal){
      ;
    }
    else{
		var name__=cur_frm.doc.name
cur_frm.add_custom_button(("Vehicle Servicing Log"),function(ev){
	frappe.set_route("List","Vehicle Servicing Log",{"vehicle":name__})
},("Show"))
cur_frm.add_custom_button(("Vehicle Trip Log"),function(ev){
	frappe.set_route("List","Vehicle Trip Log",{"vehicle":name__})
},("Show"))
cur_frm.add_custom_button(("Vehicle Servicing Log"),function(ev){
	frappe.new_doc("Vehicle Servicing Log")
},("Create"))
cur_frm.add_custom_button(("Vehicle Trip Log"),function(ev){
doc=frappe.new_doc("Vehicle Trip Log")
},("Create"))
}
},
insurance_detail:function(frm){
  console.log("entered");
},
// employee:function(frm){
//   let employee_name_=cur_frm.doc.employee
//     frappe.call({
//       method:"frappe.client.get_value",
//       args:{
//         doctype:"Employee",
//        filters:{
//          name:employee_name_,
//        },
//       fieldname:"employee_name",
//     },
//     callback:function(r){
//       var full_name=r.message["employee_name"]
//       cur_frm.set_value("employee",full_name)
//       cur_frm.refresh_field("employee")
//     }
//    })
//  },
chassis_no:function(frm){
  console.log("Starting...");
  var length=cur_frm.doc.chassis_no.length

  if(length>17 || length <17){
    cur_frm.doc.chassis_no="";
    cur_frm.refresh_field("chassis_no")
    frappe.throw("Please enter a standard Vehicle Chassis Number")
   }
},
acquisition_date:function(frm){
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
var docdate=cur_frm.doc.acquisition_date
if(docdate>today){
  cur_frm.doc.acquisition_date=""
  cur_frm.refresh_field("acquisition_date")
  frappe.throw("Selected date cannot be in the future.")
}
},
carbon_check_date:function(frm){
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
  var docdate=cur_frm.doc.carbon_check_date
  if(docdate>today){
    cur_frm.doc.carbon_check_date=""
    cur_frm.refresh_field("carbon_check_date")
    frappe.throw("Selected date cannot be in the future.")
  }

}
 // vehicle_model:function(frm){
 //   var name_=cur_frm.doc.vehicle_model+"_"+cur_frm.doc.license_plate
 //   cur_frm.set_value("vehicle_name",name_)
 //   console.log("name is: ",name_);
 //   console.log(cur_frm.doc.vehicle_name);
 //  }
}),
frappe.ui.form.on("Insurance Detail",{
  policy_end_date:function(frm,cdt,cdn){
    console.log("hola");
  for(var i=0;i<cur_frm.doc.insurance_detail.length;i++){
    var start_date=cur_frm.doc.insurance_detail[i].policy_start_date
    var end_date=cur_frm.doc.insurance_detail[i].policy_end_date
  //  console.log(start_date,end_date);
    if(end_date<start_date){
      cur_frm.doc.insurance_detail[i].policy_end_date=""
      cur_frm.refresh_field("insurance_detail")
      frappe.throw("Policy end date cannot be before policy start date")
    }
  }
  }
})
