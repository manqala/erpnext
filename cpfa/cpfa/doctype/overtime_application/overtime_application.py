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
