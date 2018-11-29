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
employee:function(frm){
  let employee_name_=cur_frm.doc.employee
    frappe.call({
      method:"frappe.client.get_value",
      args:{
        doctype:"Employee",
       filters:{
         name:employee_name_,
       },
      fieldname:"employee_name",
    },
    callback:function(r){
      var full_name=r.message["employee_name"]
      cur_frm.set_value("employee",full_name)
      cur_frm.refresh_field("employee")
    }
   })
 },
 before_save:function(frm){
   var doc_name=cur_frm.doc.vehicle_model+"_"+cur_frm.doc.license_plate
   cur_frm.set_value("vehicle_name",doc_name)
  }
})
