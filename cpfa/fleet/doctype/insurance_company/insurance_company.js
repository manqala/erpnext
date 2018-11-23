// Copyright (c) 2018, frappe and contributors
// For license information, please see license.txt

frappe.ui.form.on('Insurance Company', {
	refresh: function(frm) {
	if (!cur_frm.doc.__islocal) {
		frappe.call({
		 	args:{"name_of_company":cur_frm.doc.name},
		 		method: "cpfa.utils.misc_methods.address_loader",
		 	callback: function(r){

	   var i =0;
		 while(i<r.mes/>"sage.length){
			    var template_="<br /> <div><small> Address 1:"+r.message[i].address_line1+"</small><br />"+
				  		"<small> Address 2:"+r.message[i].address_line2+"</small><br />"+
				 		"<small> City: "+r.message[i].city+"</small><br />"+
				   	  "<small> State: "+r.message[i].state+"</small><br />"+
				   		"<small> country: "+r.message[i].country+"</small><br />"+
				   		"<small> Email:" +r.message[i].email_id+"</small><br />"+
				   		"<small>Phone:" +r.message[i].phone+"</small><br />"+
				   	 "<small> Fax:" +r.message[i].fax+"</small><br /></div> <br />";
				 var temp="";
				 temp+=template_
			i++
		 }
		 $(cur_frm.fields_dict['address_'].wrapper)
			 .html(temp);
						 refresh_field("add")
		// // 	console.log(r.message);
		console.log(r.message);
		 	}
	})
					}
								$(cur_frm.fields_dict['contact'].wrapper)
									.html("<div><p><b>First paragraph</b></p><p>Second paragraph</p><p>Third paragraph</p></div>");
},
				add_contact:function(frm){

				},
				add_address:function(frm){
					var name_=cur_frm.doc.company_name
					frappe.call({
						args:{"name_":cur_frm.doc.company_name},
						method:"cpfa.utils.misc_methods.loader",
						callback:function(r){
							var doc=frappe.model.sync(r.message)
							 // frappe.route_options={"links":r.message}
							 frappe.set_route("Form","Address", r.message.name)
						}
					})
				}
})
