# -*- coding: utf-8 -*-
# Copyright (c) 2018, frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class VehicleRequest(Document):
	pass



@frappe.whitelist()
def getEmployeeName():
	query="Select employee_name from `tabEmployee`"
	result=frappe.db.sql(query,as_dict=True)
	result_list=[]
	for i in result:
		result_list.append(i.employee_name)
	return result_list
	
