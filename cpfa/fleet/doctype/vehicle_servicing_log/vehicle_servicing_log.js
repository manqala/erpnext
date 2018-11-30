// Copyright (c) 2018, frappe and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Vehicle Servicing Log","vehicle", function(frm){
// 	frappe.model.with_doc("Service Plan Template",frm.doc.vehicle,function(){
// 		var tabletransfer=frappe.model.get_doc("Service Plan Template", frm.doc.vehicle)
	// 	$.each(tabletransfer.service_plan_,function(index,row)
	// {
	// 	d=frm.add_child("Service Details")
	// 	d.service_item=row.service_item
	// 	d.type=row.doctype
	// 	cur_frm.refresh_field("service_details")
	// })

frappe.ui.form.on("Vehicle Servicing Log",{
		vehicle:function (frm) {
		var vehicle_name=cur_frm.doc.vehicle
		if(vehicle_name==undefined){
		frappe.throw("Vehicle field must have a valid value")
	}
		frappe.call({
			args:{vehicle_name:vehicle_name},
			method:'cpfa.utils.misc_methods.getServicePlan',
			callback:function(response){
			cur_frm.clear_table("service_details")
					for(var o=0;o<=response.message[0].length-1;o++){
						frm.add_child("service_details")
						cur_frm.doc.service_details[o].service_item=response.message[0][o]
						cur_frm.doc.service_details[o].type=response.message[1][o]
						cur_frm.refresh_field("service_details")
						console.log(response.message[1]);
					}
			}
		})
	},
	before_save:function(frm){
	  console.log("Calculating");
	    var doc_ser_det=cur_frm.doc.service_details
	    var service_details_arr=Object.values(doc_ser_det)
	    var sum=0;
	    for(var i in service_details_arr){
	      var tempsum=service_details_arr[i].expense
	      sum=sum+tempsum
	    }
	    cur_frm.set_value("total_expense",sum)
	    console.log("Finished Calculation");
	    frappe.call({
	        "method": "frappe.client.set_value",
	        "args": {
	            "doctype": "Vehicle",
	            "name": cur_frm.doc.vehicle,
	            "fieldname": {
	               "odometer_value":cur_frm.doc.odometer,
	              "date_of_last_service":cur_frm.doc.service_date
	              //console.log(cur_frm.doc.service_date);

	            }
	        }
	    });
	    console.log("ran to the end");
	  },
		refresh:function(frm){
				for(var i in cur_frm.doc){
					frm.set_df_property(i, "read_only", frm.doc.__islocal ? 0 : 1);
				}
		}
})

// frappe.ui.form.on("Vehicle Service Template", "refresh", function(frm) {
// 	frappe.ui.form.on("Service Details", {
// 			"service_item": function(frm) {
// 			frm.add_fetch("[CHILD_TABLE_LINK FIELD]", "[SOURCE_CUSTOM_FIELD2]", "[TARGET_CUSTOM_FIELD2]");
// 		}
// 	});
//
// });
