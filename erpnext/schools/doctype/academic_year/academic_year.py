# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe Technologies and contributors
# For license information, please see license.txt


from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils.data import date_diff

class AcademicYear(Document):
	def validate(self):
		if date_diff(self.year_start_date, self.year_end_date) > 0:
			frappe.throw(_('Please make sure year start date is earlier than year end date.'))
