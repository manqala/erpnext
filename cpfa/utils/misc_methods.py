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
#
# def change_auto_name(self,ev):
# 	# """This function changes the default naming series of the vehicle model when it is created"""
	# name_1=self.name1
	# year_1=self.model_year
	# self.vmn=name_1+"-"+str(year_1)
	# self.name=self.vmn
	# return

def setVehicleName(self,ev):
	"""This function concantenates the licence plate and model of every vehicle created"""
	licence_plate=self.license_plate
	model=self.vehicle_model
	self.name=model+"_"+licence_plate
	#frappe.msgprint("Name set")
	return self.name

# @frappe.whitelist()
# def getVehicleModel(make_):
# 	"""This returns the model/models of a vehicle when the make is selected"""
# 	query="SELECT * from `tabVehicle Model` where vehicle_make='%s'" %make_
# 	result1=frappe.db.sql(query,as_dict=1)
# 	result2=[]
# 	for i in result1:
# 		result2.append(i.name1)#name1 is the column name of the model in the database
# 	result3=list(filter(lambda x:x!=None and x!=make_,result2))
# 	return(result3)

# def setMileage(self,ev):
# 	#This method sets the mileage value from a car after being serviced.
# 	vehicle_=frappe.get_doc("Vehicle",self.vehicle)
# 	vehicle_.last_odometer=self.odometer
# 	vehicle_.save()
# 	return

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
def loader(name_):
    new_insurance_company=frappe.new_doc("Insurance Company")
    dynamic_address=frappe.new_doc("Address")
    new_insurance_company.company_name=name_
    new_insurance_company.save()
    dynamic_address.append('links',{
    	'link_doctype':"Insurance Company",
    	'link_name':name_
    })
    dynamic_address.doctype_name=name_
    return dynamic_address
@frappe.whitelist()
def loader2(name_):
	dynamic_address=frappe.new_doc("Address")
	dynamic_address.doctype_name=name_
	return(dynamic_address)

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
def getList(request_obj):
	doc=frappe.get_doc("Vehicle Request",request_obj)
	lst=[]
	lst.append(doc.vehicle_assigned)
	lst.append(doc.employee)
	date_=doc.date_required
	dae_=date_.strftime("%d"+"-"+"%m"+"-"+"%Y")
	lst.append(doc.driver_assigned)
	lst.append(dae_)
	vehi=frappe.get_doc("Vehicle",doc.vehicle_assigned)
	lst.append(vehi.odometer_value_uom)
	return(lst)

@frappe.whitelist()
def getMileage(vehicle):
	mileage=frappe.get_value("Vehicle",vehicle,"odometer_value")
	return(mileage)

def autoname(doc,method):
	# print '\n\n\nautoname', 'method', '\n\n\n'
	doc.name = doc.vehicle_model+'_'+doc.license_plate
