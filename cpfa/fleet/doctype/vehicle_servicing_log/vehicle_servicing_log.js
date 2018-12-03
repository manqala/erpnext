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
						cur_frm.set_value("mileage_uom",response.message[2])
						console.log(response.message);
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
	               "odometer_value":cur_frm.doc.mileage,
	              "date_of_last_service":cur_frm.doc.service_date
	              //console.log(cur_frm.doc.service_date);

	            }
	        }
	    });
	    //console.log("ran to the end");
	  },
		return_date:function(frm){
			console.log(frm.doc.return_date);
		},
		refresh:function(frm){
				for(var i in cur_frm.doc){
					frm.set_df_property(i, "read_only", frm.doc.__islocal ? 0 : 1);
				}
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
				cur_frm.set_value("service_date",today)
		},
		expected_return_date:function(frm){
			let service_date=cur_frm.doc.service_date
			if(service_date>cur_frm.doc.expected_return_date){
				cur_frm.doc.expected_return_date=""
				cur_frm.refresh_field("expected_return_date")
				frappe.throw("Expected return date cannot be before service date")
			}
		},
		mileage:function(frm){
			var vehicle =frm.doc.vehicle
			cur_val=frm.doc.mileage
			frappe.call({
				method:"cpfa.utils.misc_methods.getMileage",
				args:{vehicle:vehicle},
				callback:function(r){
				if(cur_val<r.message){
					frm.doc.mileage=""
					cur_frm.refresh_field("mileage")
					frappe.throw("Inputted value is less than current mileage value,Enter a valid value for mileage.")
				}
				}
			})
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
