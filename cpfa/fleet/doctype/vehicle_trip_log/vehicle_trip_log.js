// Copyright (c) 2018, Manqala and contributors
// For license information, please see license.txt

frappe.ui.form.on('Vehicle Trip Log', {
	refresh: function(frm) {
console.log("welcome");
},
validate:function(frm){
	var refueling_detail=cur_frm.doc.refueling_detail;
	var ts=2
	for(var i in refueling_detail){
	var v1=refueling_detail[i].fuel_price
	var v2=refueling_detail[i].fuel_quantity
		refueling_detail[i].total=parseInt(v1*v2)
		cur_frm.refresh_field("refueling_detail")

	}
}
});
