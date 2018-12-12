// Copyright (c) 2018, frappe and contributors
// Fo r license information, please see license.txt

 frappe.ui.form.on('Vehicle Request', {
   refresh:function(frm){
     frm.set_df_property("employee","read_only",frm.doc.__islocal ? 0 : 1)
     if(frm.doc.__islocal){
       ;
       if(frm.doc.vehicle_type_required){
         cur_frm.set_query("vehicle_assigned",function(){
           return {
             filters:{
               "vehicle_type":cur_frm.doc.vehicle_type_required,
               "status":"available",
             }
           }
         })
       }
     }
     else{
       cur_frm.add_custom_button(("Vehicle Trip Log"),function(ev){
         var docname=cur_frm.doc.name
         var employee=frm.doc.employee
         var driver=frm.doc.driver_assigned
         var vehicle=frm.doc.vehicle_assigned
         var date=frm.doc.date_required
      frappe.call({
        method:"cpfa.fleet.doctype.vehicle_request.vehicle_request.getTripLog",
        args:{docname:docname,employee:employee,driver:driver,vehicle:vehicle,date:date},
        callback:function(r){
          var doc=frappe.model.sync(r.message)
          frappe.set_route("Form","Vehicle Trip Log", r.message.name)
        }
      })
       },("Create"))
     }
   },
   employee:function(frm){
     if(frm.doc.employee==undefined){
       ;
     }
     else{
     frappe.call({
       method:"cpfa.fleet.doctype.vehicle_request.vehicle_request.get_value",
       args:{
         doctype:"Employee",
         docname:frm.doc.employee,
         fieldname:"employee_name"
       },
       callback:function(r){
         cur_frm.set_value("employee_name",r.message)
       }
     })
   }
 },
    date_required:function(frm) {
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
   	var docdate=cur_frm.doc.date_required
   	if(docdate<today){
   	  cur_frm.doc.date_required=""
   	  cur_frm.refresh_field("date_required")
   	  frappe.throw("Selected date cannot be in the past.")
   	}
   	else{
   	}
   },
   vehicle_type_required: function(frm){
     cur_frm.set_query("vehicle_assigned",function(){
       return {
         filters:{
           "vehicle_type":cur_frm.doc.vehicle_type_required,
           "status":"available",
         }
       }
     })
 }

   });
// 	refresh: function(frm) {
// 		frappe.call({
// 			args:{},
// 			method:"cpfa.fleet.doctype.vehicle_request.vehicle_request.getEmployeeName",
// 			callback:function(r){
// 			cur_frm.set_df_property("employee_name","options",r.message)
// 			cur_frm.refresh_field("employee_name")
// 			//console.log(r.message)
// 			}
// 		})
// 	},
	// employee_name:function(frm){
	// 	frappe.call({
	// 		method:"frappe.client.get_value",
	// 		args:{
	// 			doctype:"Employee",
	// 			filters:{employee_name:cur_frm.doc.employee_name},
	// 			fieldname:['user_id',"name","prefered_email"],
	// 		},
	// 		callback: function(r){
	// 			console.log(r.message);
	//
	// 			if(r.message.user_id==null){
	// 				cur_frm.set_value("employee_email",r.message.prefered_email)
	// 			}
	// 			else{
	// 				cur_frm.set_value("employee_email",r.message.user_id)
	// 			}
	// 			cur_frm.set_value("employee",r.message.name)
	// 		}
	//
	// 	})
	// }

// time_required:function(frm){
// 	var today = new Date();
// 	var dd = today.getDate();
// 	var mm = today.getMonth()+1; //January is 0!
// 	var yyyy = today.getFullYear();
// 	if(dd<10) {
// 	    dd = '0'+dd
// 	}
// 	if(mm<10) {
// 	    mm = '0'+mm
// 	}
// 	today = yyyy + '-' + mm + '-' + dd;
// 	time_now=new Date().getHours()+":"+new Date().getMinutes()+":"+new Date().getSeconds()
// 	console.log(time_now);
// 	console.log(cur_frm.doc.time_required);
// }
