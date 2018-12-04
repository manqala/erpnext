 // Copyright (c) 2018, Manqala and contributors
// For license information, please see license.txt

frappe.ui.form.on('Vehicle Trip Log', {
// 	refresh: function(frm) {
// 		for(var i in cur_frm.doc){
// 			frm.set_df_property(i, "read_only", frm.doc.__islocal ? 0 : 1);
// 		}
// 		if(cur_frm.doc.__islocal){
// 			console.log("unsaved");
// 		}
// 		else{
// 			console.log("saved");
// 		}
// },
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
	var trip_type=frm.doc.trip_type;
if(trip_type=="Trip"){
	;
}
else{
	var refueling_detail=cur_frm.doc.refueling_detail;
	for(var i=0;i<refueling_detail.length;i++){
	var v1=refueling_detail[i].fuel_price
	var v2=refueling_detail[i].fuel_quantity
	refueling_detail[i].total=v1*v2
	}
	 cur_frm.refresh_field("refueling_detail")
	 var sum=0;
	 for(var o=0; o<refueling_detail.length;o++){
 sum+=refueling_detail[o].total
}
cur_frm.set_value("trip_expense",sum)
console.log(sum);
}

},
 vehicle_request:function(frm){
 var request_obj=cur_frm.doc.vehicle_request
 console.log(request_obj);
 	 frappe.call({
 		method:"cpfa.utils.misc_methods.getList",
		args:{request_obj:request_obj},
		callback:function(r){
		console.log(r.message);
 		cur_frm.set_value("vehicle",r.message[0])
		cur_frm.set_value("employee",r.message[1])
		cur_frm.set_value("driver",r.message[2])
		//cur_frm.set_value("trip_started",r.message[3])
		 var t=r.message[3]
	console.log(t);

		 cur_frm.set_value("mileage_uom",r.message[4])
  		}
 	})
 },
 trip_started:function(frm){
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
	 if(frm.doc.trip_started>today){
		 frm.doc.trip_started=""
		 cur_frm.refresh_field("trip_started")
		 frappe.throw("You cannot log a vehicle trip for a future date.")
	 }
 },
trip_ended:function(frm){
	start_date=cur_frm.doc.trip_started
	if(start_date>cur_frm.doc.trip_ended){
		cur_frm.doc.trip_ended=""
		cur_frm.refresh_field("trip_ended")
		frappe.throw("Date of trip ending cannot be before date trip started")
	}
}
});
