 // Copyright (c) 2018, Manqala and contributors
// For license information, please see license.txt

frappe.ui.form.on('Vehicle Trip Log', {
	refresh: function(frm) {
		for(var i in cur_frm.doc){
			frm.set_df_property(i, "read_only", frm.doc.__islocal ? 0 : 1);
		}
},
incidents:function(frm){
	if(cur_frm.doc.incidents==0)
		{
			cur_frm.toggle_display("incidents_description",false);
		}
		else{
			cur_frm.toggle_display("incidents_description",true)
		}
},
validate:function(frm){
	 var refueling_detail=cur_frm.doc.refueling_detail;
	 for(var i in refueling_detail.length){
	 var v1=refueling_detail[i].fuel_price
	 var v2=refueling_detail[i].fuel_quantity
	 refueling_detail[i].total=v1*v2
	// 	console.log("called");
	 }
	 	cur_frm.refresh_field("refueling_detail")
		var sum=0;
		for(var o=0; o<refueling_detail.length;o++){
	sum+=refueling_detail[o].total
}
cur_frm.set_value("trip_expense",sum)
console.log(sum);
},
vehicle_request:function(frm){
	var request_obj=cur_frm.doc.vehicle_request
	frappe.call({
		method:"frappe.client.get_value",
		args:{
			doctype:"Vehicle Request",
			filters:{
				name:request_obj,
			},
			fieldname:["employee","driver_assigned","vehicle_assigned"]
		},
		callback:function(r){
			cur_frm.set_value("employee",r.message.employee)
			cur_frm.set_value("vehicle",r.message.vehicle_assigned)
			cur_frm.set_value("driver",r.message.driver_assigned)
		}
	})
}
});
