// Copyright (c) 2018, frappe and contributors
// For license information, please see license.txt

frappe.ui.form.on('Insurance Company', {
	refresh: function(frm) {
 	if (!cur_frm.doc.__islocal) {
 		cur_frm.add_custom_button(("Address"),function(ev){
		 	frappe.set_route("List","Address",{"doctype_name":cur_frm.doc.name})
		 },("Edit"))
		cur_frm.add_custom_button(("Contact"),function(ev){
		frappe.set_route("List","Contact",{"doctype_name":cur_frm.doc.name})
		},("Edit"))
 		frappe.call({
	 	 	args:{"name_of_company":cur_frm.doc.name},
	 	 		method:"cpfa.utils.misc_methods.address_loader",
	 	 	callback: function(r){
				if(r.message==undefined){
					$(cur_frm.fields_dict['address'].wrapper)
 		 			 .html("");
 								 cur_frm.refresh_field("address")
				}
				else{
			var temp="";
		    var i =0;
		 		 while(i<r.message.length){
					  var template_="<br /> <div><b>"+(i+1)+" "+r.message[i].address_type+"</b><br />"+
						"<small> "+r.message[i].address_line1+"</small><br />"+
					 		"<small>"+r.message[i].address_line2+"</small><br />"+
					 	"<small> "+r.message[i].city+"</small><br />"+
					 		"<small>"+r.message[i].state+"</small><br />"+
					 		"<small>"+r.message[i].country+"</small><br />"+
					 		"<small>" +r.message[i].email_id+"</small><br />"+
					 		"<small>" +r.message[i].phone+"</small><br />"+
					 	 "<small>" +r.message[i].fax+"</small><br /></div> <br />";
						 temp+=template_
					 i++
		 		 }
		 		 $(cur_frm.fields_dict['address'].wrapper)
		 			 .html(temp);
								 cur_frm.refresh_field("address")

				}

	 	 }
	 })
	 frappe.call({
	 	args:{"name_of_company":cur_frm.doc.name},
	 	method:'cpfa.utils.misc_methods.contact_loader',
	 	callback:function(r){
		if(r.message==undefined){
			$(cur_frm.fields_dict['contact'].wrapper)
				 .html("");
				 cur_frm.refresh_field("contact")
		}
		else{
			con_temp="";
	 		var i=0;
	 			while(i<r.message.length){
	  			  var template_="<br /> <div><b>"+r.message[i].first_name+" "+r.message[i].last_name+"</b><br />"+
	  				"<small> "+r.message[i].phone+"</small><br />"+
	  			 		"<small>"+r.message[i].mobile_no+"</small><br />"+
	  			 	"<small> "+r.message[i].email_id+"</small><br /></div> <br />";
	  				 con_temp+=template_
	  			 i++
	  		 }
	 		 $(cur_frm.fields_dict['contact'].wrapper)
	 				.html(con_temp);
	 				cur_frm.refresh_field("contact")
		}

			}
 	})
}
else{
	$(cur_frm.fields_dict['contact'].wrapper)
		 .html("");
		 $(cur_frm.fields_dict['address'].wrapper)
		 	.html("");
}
},
				add_contact:function(frm){
					if(!cur_frm.doc.__islocal){
					 	console.log("saved");
						frappe.call({
						args:{name_:cur_frm.doc.company_name,target_doctype:"Contact"},
						method:"cpfa.utils.misc_methods.loader2",
						callback:function(r){
							let doc=frappe.model.sync(r.message);
							frappe.set_route("Form","Contact",r.message.name)
						}
					})
				}
				else{
				 	console.log("unsaved");
					if(frm.doc.company_name==undefined){
						frappe.throw("Insurance Company field cannot be empty")
					}
					frappe.call({
					args:{name_:cur_frm.doc.company_name,location_doctype:cur_frm.doc.doctype,target_doctype:"Contact"},
					method:"cpfa.utils.misc_methods.loader",
					callback:function(r){
						var doc=frappe.model.sync(r.message)
						 frappe.set_route("Form","Contact", r.message.name)
					}
				})
				}
				},
				add_address:function(frm){
					if(!cur_frm.doc.__islocal){
						console.log("saved");
						frappe.call({
							args:{name_:cur_frm.doc.company_name,target_doctype:"Address"},
							method:"cpfa.utils.misc_methods.loader2",
							callback:function(r){
								var doc=frappe.model.sync(r.message)
								 // frappe.route_options={"links":r.message}
								 frappe.set_route("Form","Address", r.message.name)
							}
						})
					}
					else{
						console.log("unsaved");
						if(frm.doc.company_name==undefined){
							frappe.throw("Insurance Company field cannot be empty")
						}
					frappe.call({
						args:{name_:cur_frm.doc.company_name,location_doctype:cur_frm.doc.doctype,target_doctype:"Address"},
						method:"cpfa.utils.misc_methods.loader",
						callback:function(r){
							var doc=frappe.model.sync(r.message)
							 // frappe.route_options={"links":r.message}
							 frappe.set_route("Form","Address", r.message.name)
						}
					})
				}
				}
})
