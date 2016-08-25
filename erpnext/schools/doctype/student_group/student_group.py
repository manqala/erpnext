# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _
from erpnext.schools.utils import validate_duplicate_student

class StudentGroup(Document):
	def autoname(self):
		self.name = self.student_group_name
	
	def validate(self):
		self.validate_strength()
		self.validate_student_name()
		validate_duplicate_student(self.students)

	def validate_strength(self):
		if self.max_strength and len(self.students) > self.max_strength:
			frappe.throw(_("""Cannot enroll more than {0} students for this student group.""").format(self.max_strength))

	def validate_student_name(self):
		for d in self.students:
			d.student_name = frappe.db.get_value("Student", d.student, "title")
	
	