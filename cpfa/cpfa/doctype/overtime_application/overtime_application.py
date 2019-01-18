# -*- coding: utf-8 -*-
# Copyright (c) 2019, Manqala and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


@frappe.whitelist()
def date_append(date):
	return(str(type(date)))

class OvertimeApplication(Document):
	pass
	def autoname(self):
		self.name=self.employee_name+"_"+self.date
	def validate(self):
		if(self.expected_period_of_task<4):
			frappe.msgprint("Overtime duration that is less than 4 hours does not qualify for overtime allowance")
            
