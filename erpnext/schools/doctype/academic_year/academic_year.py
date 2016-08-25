# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document

class AcademicYear(Document):
	def validate(self):
		from datetime import datetime
		start_date = datetime.strptime(self.year_start_date,'%Y-%m-%d')
		end_date = datetime.strptime(self.year_end_date,'%Y-%m-%d')
		if start_date > end_date:
			frappe.throw(_('Please make sure start date is earlier than end date!'))
