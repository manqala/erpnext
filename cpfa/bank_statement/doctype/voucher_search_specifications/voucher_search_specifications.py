# -*- coding: utf-8 -*-
# Copyright (c) 2018, Manqala and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import cint
from datetime import datetime


class VoucherSearchSpecifications(Document):
	def __init__(self, *args, **kwargs):
		super(VoucherSearchSpecifications, self).__init__(*args, **kwargs)
		self.flags.ignore_links = True

	def get_spec_row(self, key, val):
		return next((r for r in self.voucher_search_keys if \
					 r.get(key)==val),None)

	def transform_fields(self, dn, idx=None):
		row = self.get_spec_row('name', dn)
		if not row:
			return
		duplicate = False
		res = []
		for i in range(1, 11):
			field = 'field_%s'%i
			eval_rule_field = field + '_transformation_rule'
			field_val = row.get(field, '')
			if field_val:
				# check if the selected already exists
				if (idx != None) and cint(idx) != i:
					if field_val == row.get('field_%s'%idx):
						frappe.msgprint('Field: %s already selected in Field %s'%(field_val,field))
						row.set('field_%s'%idx, '')
						duplicate = True
						break

				if row.get(eval_rule_field, ''):
					res.append(self.transform_field(field, dn) or '')
				else:
					res.append(field_val)
		if not duplicate:
			return (row.separator or '-').join(map(str, res))
		return row.search_key_specification

	def transform_field(self, field, dn):
		eval_rule_field = field + '_transformation_rule'
		row = self.get_spec_row('name', dn)
		if not row:
			return
		field_val = row.get(field, '')
		eval_code = row.get(eval_rule_field, '')
		docfield = frappe.get_meta(row.voucher_type).get_field(field_val)
		if docfield:
			if docfield.fieldtype == 'Date':
				field_val = datetime.now().date()
			elif docfield.fieldtype == 'Time':
				field_val = datetime.now().time()
		if not eval_code:
			return

		eval_data = {field: field_val}
		
		try:
			return frappe.safe_eval(eval_code, None, eval_data)

		except NameError as err:
			frappe.throw(_("Name error: {0}".format(err)))
		except SyntaxError as err:
			frappe.throw(_("Syntax error in formula or condition: {0}".format(err)))
		except Exception as e:
			frappe.throw(_("Error in formula or condition: {0}".format(e)))

	def get_search_key(self, doc, doctype=None):
		"""returns a key as specified in the search key spec"""
		vals = []
		row = self.get_spec_row('voucher_type', doctype or doc.doctype)
		if not row:
			return
		for i in range(1, 11): #for fields field_1 to field_10
			field = 'field_%s'%i
			eval_rule_field = field + '_transformation_rule'
			field_name = row.get(field, '')
			eval_rule = row.get(eval_rule_field, '')
			if field_name:
				val = doc.get(field_name)
				if eval_rule and val != None:
					eval_rule = eval_rule.replace(field, field_name)
					eval_data = {field_name: val}
					val = frappe.safe_eval(eval_rule, None, eval_data)
				if val != None:
					vals.append(val)
		return (row.separator or '-').join(map(str, vals))

	def get_voucher_fields(self):
		v_fields = {}
		for row in self.voucher_search_keys:
			fields = []
			for i in xrange(1,11):
				field = row.get('field_%s'%i)
				if field:
					fields.append(field)
			if fields:
				v_fields[row.voucher_type] = fields
		return v_fields
