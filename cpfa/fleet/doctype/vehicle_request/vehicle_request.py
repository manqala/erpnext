# -*- coding: utf-8 -*-
# Copyright (c) 2018, frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class VehicleRequest(Document):
	pass

	def autoname(self):
		name=frappe.get_value("Employee",self.employee,"employee_name")
		self.name=name+self.date_required
		return




@frappe.whitelist()
def getTripLog(docname,employee,driver,vehicle,date):
	triplog=frappe.new_doc("Vehicle Trip Log")
	triplog.vehicle_request=docname
	triplog.employee=employee
	triplog.driver=driver
	triplog.vehicle=vehicle
	triplog.trip_started=date
	odometer_uom=frappe.get_doc("Vehicle",vehicle).odometer_value_uom
	triplog.mileage_uom=odometer_uom
	return(triplog)
