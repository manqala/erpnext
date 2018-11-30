from __future__ import unicode_literals
import frappe
import datetime


def set_vehicle_status():
	print("Starting......")
	query="Select * from `tabVehicle Request` where status='Approved'"
	result_set=frappe.db.sql(query,as_dict=1)
	today=datetime.date.today()
	for i in result_set:
		if i.date_required==today:
			employee=i.employee
			vehicle=i.vehicle_required
			required_vehicle=frappe.get_doc("Vehicle",vehicle)
			required_vehicle.status="Reserved"
			required_vehicle.employee=employee
			required_vehicle.save()
	print("Sucessful!!")
