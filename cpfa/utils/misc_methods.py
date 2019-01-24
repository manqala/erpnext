import frappe
import datetime

@frappe.whitelist()
def get_days_present(employee,cal_end,cal_start):
	"""Here we write queries that collect attendance data of an employee from the database"""
	num1=frappe.db.sql("select count(*) from tabAttendance where employee_name=%s and status='Absent' and attendance_date>=%s and attendance_date<=%s ",(employee,cal_start,cal_end))
	num=num1[0]
	number=num[0]
	sal=frappe.db.sql("Select base from `tabSalary Structure Employee` where employee_name=%s",(employee))
	sal1=sal[0]
	salary=sal1[0]
	package=[number,salary]
	return package

def calculate_base_amount(salary_doc, event):
	"""This calculates the amount an employee earns according to his/her attendance in a month"""
	query = "Select base from `tabSalary Structure Employee` where employee='%s'" %salary_doc.employee
	query2="SELECT COUNT(*)from tabAttendance where employee_name='%s' and status='Absent' and attendance_date>='%s' and attendance_date<='%s'" %(salary_doc.employee_name,salary_doc.start_date,salary_doc.end_date)
	sal2=frappe.db.sql(query2)
	sal=frappe.db.sql(query, as_dict=1)
	if sal2:
		salary_doc.number_of_days_missed=sal2[0][0]
	if sal:
		salary_doc.annual_salary=sal[0].base
		monthly_sal=sal[0].base/12
		daily_pay=monthly_sal/salary_doc.total_working_days
		net_deduc=daily_pay*sal2[0][0]
		salary_doc.salary_for_month=monthly_sal-net_deduc
	return

def setVehicleName(self,ev):
	"""This function concantenates the licence plate and model of every vehicle created"""
	licence_plate=self.license_plate
	model=self.vehicle_model
	self.name=model+"_"+licence_plate
	#frappe.msgprint("Name set")
	return self.name



@frappe.whitelist()
def getServicePlan(vehicle_name):
	current_vehicle=frappe.get_doc("Vehicle",vehicle_name)
	vehicle_model=current_vehicle.vehicle_model
	odometer_uom=current_vehicle.odometer_value_uom
	query1="select service_item,type,name from `tabService Plan Template` where  parent='%s' " %vehicle_model
	result_set=frappe.db.sql(query1,as_dict=1)
	service_item_list=[]
	service_type_list=[]
	name_list=[]
	for i in result_set:
		service_item_list.append(i.service_item)
	for i in result_set:
		service_type_list.append(i.type)
	container=[]
	container.append(service_item_list)
	container.append(service_type_list)
	container.append(odometer_uom)
	return(container)

@frappe.whitelist()
def loader(name_,target_doctype,location_doctype):
    new_location=frappe.new_doc(location_doctype)
    new_target=frappe.new_doc(target_doctype)
    new_location.company_name=name_
    new_location.save()
    # dynamic_address.append('links',{
    # 	'link_doctype':"Insurance Company",
    # 	'link_name':name_
    # })
    new_target.doctype_name=name_
    return(new_target)
@frappe.whitelist()
def loader2(name_,target_doctype):
	new_target=frappe.new_doc(target_doctype)
	new_target.doctype_name=name_
	return(new_target)

@frappe.whitelist()
def address_loader(name_of_company):
	result=frappe.get_all("Address",filters={"doctype_name":name_of_company},fields=["address_type","address_line1","address_line2","city","state","country","email_id","phone","fax"])
	if result:
		return(result)
	else:
		return None
@frappe.whitelist()
def contact_loader(name_of_company):
	result=frappe.get_all("Contact",filters={"doctype_name":name_of_company},fields=["first_name","last_name","phone","mobile_no","email_id"])
	if result:
		return(result)
	else:
		return None

@frappe.whitelist()
def getContacts(name_):
	new_contact=frappe.new_doc("Contact")
	new_contact.doctype_name=name_
	return(new_contact)


@frappe.whitelist()
def getMileage(vehicle):
	mileage=frappe.get_value("Vehicle",vehicle,"odometer_value")
	return(mileage)

@frappe.whitelist()
def getType(model):
	result=frappe.get_value("Vehicle Model",model,"vehicle_type")
	return(result)
	frappe.throw("No vehicle request data recieved!")

@frappe.whitelist()
def new_vsl(docname,doctype,vehicle_model):
	new_vsl=frappe.new_doc(doctype)
	new_vsl.vehicle=docname
	vehicle=frappe.get_doc("Vehicle",docname)
	odometer_value=vehicle.odometer_value_uom
	new_vsl.mileage_uom=odometer_value
	query1="select service_item,type,name from `tabService Plan Template` where  parent='%s' " %vehicle_model
	result_set=frappe.db.sql(query1,as_dict=1)
	for i in result_set:
	 	new_vsl.append("service_details",{"service_item":i.service_item,"type":i.type,"currency":"NGN"})
	return(new_vsl)

@frappe.whitelist()
def getServiceTemp(model):
	result_set=frappe.get_all("Service Plan Template",filters={"parent":model},fields=["service_item","type","frequency","mileage_interval","mileage_uom"] )
	return(result_set)

@frappe.whitelist()
def getVal(location):
	value=frappe.get_value("Vehicle Location",location,"vehicle_location")
	return(value)

@frappe.whitelist()
def getRequest(vehicle_type,vehicle_name):
	new_request=frappe.new_doc("Vehicle Request")
	new_request.vehicle_type_required=vehicle_type
	new_request.vehicle_assigned=vehicle_name
	return(new_request)

@frappe.whitelist()
def get_timesheet(employee):
	query1="Select * from `tabTimesheet` where employee='%s' and status='Submitted'" %employee
	result=frappe.db.sql(query1,as_dict=1)
	if result:
		return(result)
	else:
		return("Nothing")

@frappe.whitelist()
def get_val(emp):
	return(frappe.get_doc("Employee",emp).user_id)

def autoname(doc,method):
	# print '\n\n\nautoname', 'method', '\n\n\n'
	doc.name = doc.vehicle_make+"_"+doc.vehicle_model+'_'+doc.license_plate
	return(doc.name)
