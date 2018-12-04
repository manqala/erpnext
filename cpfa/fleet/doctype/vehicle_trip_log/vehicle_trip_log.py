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
		vehicle.save()
		return

@frappe.whitelist()
def getTripLog(docname):
	doc=frappe.new_doc("Vehicle Trip Log")
	doc.vehicle_request
	return(doc)
