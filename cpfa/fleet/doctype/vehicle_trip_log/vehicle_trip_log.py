# -*- coding: utf-8 -*-
# Copyright (c) 2018, Manqala and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class VehicleTripLog(Document):
	pass

	def validate(self):
		vehicle=frappe.get_doc("Vehicle",self.vehicle)
		vehicle.odometer_value=self.mileage
		if self.trip_type=="Trip":
			vehicle.status="Available"
		vehicle.save()
		return

@frappe.whitelist()
def getList(request_obj):
	doc=frappe.get_doc("Vehicle Request",request_obj)
	triplog=frappe.new_doc("Vehicle Trip Log")
	triplog.vehicle_request=request_obj
	triplog.employee=doc.employee
	triplog.driver=doc.driver_assigned
	triplog.vehicle=doc.vehicle_assigned
	triplog.mileage_uom=frappe.get_doc("Vehicle",doc.vehicle_assigned).odometer_value_uom
	triplog.trip_started=doc.date_required
	employee_name=frappe.get_doc("Employee",doc.employee).employee_name
	triplog.employee_name=employee_name
	return(triplog)
