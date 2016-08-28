# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe Technologies and contributors
# For license information, please see license.txt


from __future__ import unicode_literals
import frappe
<<<<<<< HEAD
from frappe import _
=======
from frappe import msgprint, _
>>>>>>> 540bae8d5bc84c0e70593efa3ae8e9f0999543f7
from frappe.model.document import Document
from frappe.utils.data import date_diff

class AcademicYear(Document):
    def validate(self):
        #Check that start of academic year is earlier than end of academic year
        if self.year_start_date and self.year_end_date and self.year_start_date > self.year_end_date:
            frappe.throw(_("The Year End Date cannot be earlier than the Year Start Date. Please correct the dates and try again."))
