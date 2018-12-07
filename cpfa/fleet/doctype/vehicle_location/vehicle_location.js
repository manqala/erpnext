// Copyright (c) 2018, frappe and contributors
// For license information, please see license.txt

frappe.ui.form.on('Vehicle Location', {
	refresh: function(frm) {
			cur_frm.refresh_field("address")
		if(!cur_frm.doc.__islocal){
		 frappe.call({
		 	method:"frappe.client.get_value",
			args:{
		 		doctype:"Address",
				filters:{
					doctype_name:cur_frm.doc.name
				},
				fieldname:["address_type","address_line1","city","state","country"]
			},
			callback:function(r){
				console.log(r.message);
				if (r.message!=undefined){
					var	template="<br /><div><b>"+r.message.address_type+"</b><br />"+
						"<small>"+r.message.address_line1+"</small><br />"+
						"<small>"+r.message.city+"</small><br />"+
						"<small>"+r.message.state+"</small><br />"+
						"<small>"+r.message.country+"</small></div><br />"
						$(cur_frm.fields_dict["address"].wrapper)
							.html(template)
							cur_frm.refresh_field("address")
						}
							else{
								$(cur_frm.fields_dict["address"].wrapper)
									.html("")
									cur_frm.refresh_field("address")
							}
				}

		 })
		}
		else{
			;
		}
		frappe.form.link_formatters['Vehicle Location'] = function(value, doc) {
			if(doc && doc.vehicle_location && doc.vehicle_location !== value) {
				return value? value + ':'+ doc.vehicle_location: doc.vehicle_location;
			} else {
				return value;
			}
		}
	},
	add_address:function(frm){
		if(cur_frm.doc.__islocal){
			frappe.throw("Please save the document first before adding address");
		}
		else{
		frappe.call({
			method:"cpfa.utils.misc_methods.loader",
			args:{"name_":cur_frm.doc.name},
			callback:function(r){
				var doc=frappe.model.sync(r.message)
				 frappe.set_route("Form","Address", r.message.name)
			}
		})
	}
}
});
