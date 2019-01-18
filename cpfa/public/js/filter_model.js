frappe.ui.form.on("Vehicle",{
  change_vehicle_location:function(frm) {
          // $(frm.fields_dict.vehicle_location.input).on('click', function(e){
            cur_frm.set_df_property("vehicle_location","read_only",false)
            cur_frm.refresh_field("vehicle_location")
          // });
      },
  vehicle_make: function(frm){
    cur_frm.set_query("vehicle_model",function(){
      return {
        filters:{
          "vehicle_make":cur_frm.doc.vehicle_make
        }
      }
    })
  },
      // cur_frm.fields_dict["vehicle_model"].get_query=function(doc){
      //   return {
      //     filters:{
      //       "vehicle_make":frm.doc.vehicle_make,
      //   }
      // }
      // }


  refresh: function(frm){
    frm.set_df_property("vehicle_location","read_only",frm.doc.__islocal ? 0 : 1)
    if(frm.doc.__islocal){
      ;
    }
    else{
      if(cur_frm.doc.vehicle_location!==undefined){
         var location=cur_frm.doc.vehicle_location
        frappe.call({
          method:"cpfa.utils.misc_methods.getVal",
          args:{location:location},
          callback:function(r){
          cur_frm.set_value("location_name",r.message)
          }
        })
      }
      else {
        ;
      }
		var name__=cur_frm.doc.name
cur_frm.add_custom_button(("Vehicle Servicing Log"),function(ev){
frappe.set_route("List","Vehicle Servicing Log",{"vehicle":name__})
},("Show"))
cur_frm.add_custom_button(("Vehicle Trip Log"),function(ev){
	frappe.set_route("List","Vehicle Trip Log",{"vehicle":name__})
},("Show"))
cur_frm.add_custom_button(("Vehicle Servicing Log"),function(ev){
docname=frm.doc.name
doctype="Vehicle Servicing Log"
vehicle_model=frm.doc.vehicle_model
  frappe.call({
    method:"cpfa.utils.misc_methods.new_vsl",
    args:{docname:docname,doctype:doctype,vehicle_model:vehicle_model},
    callback:function(r){
       var doc=frappe.model.sync(r.message)
      frappe.set_route("Form","Vehicle Servicing Log", r.message.name)
    }
  })
},("Create"))
cur_frm.add_custom_button(("Vehicle Trip Log"),function(ev){
doc=frappe.new_doc("Vehicle Trip Log")
},("Create"))
cur_frm.add_custom_button(("Vehicle Request"),function(ev){
var vehicle_type=frm.doc.vehicle_type
var vehicle_name=frm.doc.name
if(vehicle_type==undefined){
  ;
}
else{
frappe.call({
  method:"cpfa.utils.misc_methods.getRequest",
  args:{vehicle_type:vehicle_type,vehicle_name:cur_frm.doc.name},
  callback:function(r){
   var doc=frappe.model.sync(r.message)
   frappe.set_route("Form","Vehicle Request",r.message.name)
  }
})}
},("Create"))
var model=frm.doc.vehicle_model
// frappe.call({
//   method:"cpfa.utils.misc_methods.getServiceTemp",
//   args:{model:model},
//   callback:function(response){
//     cur_frm.clear_table("service_details")
//        for(var o=0;o<response.message.length;o++){
//          frm.add_child("service_details")
//          frm.doc.service_details[o].service_item=response.message[o].service_item
//          frm.doc.service_details[o].type=response.message[o].type
//          frm.doc.service_details[o].mileage_interval=response.message[o].mileage_interval
//          frm.doc.service_details[o].mileage_uom=response.message[o].mileage_uom
//          frm.doc.service_details[o].frequency=response.message[o].frequency
//        }
//          frm.refresh_field("service_details")
//        console.log(response.message.length);
//   }
// })
}
},
 vehicle_model:function(frm){
  var model=frm.doc.vehicle_model
  console.log(model);
  if(model==undefined){
    ;
  }
  else{
    frappe.call({
     method:"cpfa.utils.misc_methods.getType",
     args:{model:model},
      callback:function(response){
        cur_frm.set_value("vehicle_type",response.message)
      }
   })
   frappe.call({
     method:"cpfa.utils.misc_methods.getServiceTemp",
     args:{model:model},
     callback:function(response){
       cur_frm.clear_table("service_details")
 					for(var o=0;o<response.message.length;o++){
 						frm.add_child("service_details")
 						frm.doc.service_details[o].service_item=response.message[o].service_item
 						frm.doc.service_details[o].type=response.message[o].type
            frm.doc.service_details[o].mileage_interval=response.message[o].mileage_interval
            frm.doc.service_details[o].mileage_uom=response.message[o].mileage_uom
            frm.doc.service_details[o].frequency=response.message[o].frequency
 					}
           	frm.refresh_field("service_details")

     }
   })
  }
 },
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
vehicle_location: function(frm){
  var location=cur_frm.doc.vehicle_location
  if(location){
    frappe.call({
      method:"cpfa.utils.misc_methods.getVal",
      args:{location:location},
      callback:function(r){
      cur_frm.set_value("location_name",r.message)
      }
    })
  }
  else{
    ;
  }
},
carbon_check_date:function(frm){
  var today = new Date();
  var dd = today.getDate();
  var mm = today.getMonth()+1;
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
}),
frappe.ui.form.on("Insurance Detail",{
  policy_end_date:function(frm,cdt,cdn){
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
