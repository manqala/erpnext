from __future__ import unicode_literals
import frappe



def set_vehicle_status():
	return
	doc=frappe.get_doc("Vehicle","Pathfinder-2016_YI-896-JJN")
	doc.odometer_2=1414
	doc.save()
